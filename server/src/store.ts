import { mkdirSync } from "node:fs";
import { dirname } from "node:path";
import { DatabaseSync } from "node:sqlite";

export type InquiryStatus = "active" | "paused" | "closed";

export interface InquiryState {
  summary?: string;
  findings?: string[];
  uncertainty?: string[];
  open_questions?: string[];
  pivots?: string[];
  linked_memory_ids?: string[];
}

export interface InquiryRecord {
  id: string;
  title: string;
  focus: string;
  status: InquiryStatus;
  version: number;
  created_at: string;
  updated_at: string;
  state: InquiryState;
  status_history: Array<{
    at: string;
    from: InquiryStatus | null;
    to: InquiryStatus;
    reason?: string;
  }>;
}

export interface MemoryRecord {
  id: string;
  title: string;
  type: string;
  status: string;
  content: string;
  confidence?: string;
  source_inquiries: string[];
  tags: string[];
  related: string[];
  supersedes?: string;
  version: number;
  created_at: string;
  updated_at: string;
}

export class ConflictError extends Error {}
export class NotFoundError extends Error {}

function now(): string {
  return new Date().toISOString();
}

function slug(value: string): string {
  const normalized = value
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "")
    .slice(0, 48);
  return normalized || "untitled";
}

function parseJson<T>(value: unknown, fallback: T): T {
  if (typeof value !== "string" || value.length === 0) return fallback;
  return JSON.parse(value) as T;
}

function stringify(value: unknown): string {
  return JSON.stringify(value);
}

export class DialecticalStore {
  readonly db: DatabaseSync;

  constructor(path: string) {
    if (path !== ":memory:") mkdirSync(dirname(path), { recursive: true });
    this.db = new DatabaseSync(path);
    this.db.exec("PRAGMA foreign_keys = ON; PRAGMA journal_mode = WAL;");
    this.migrate();
  }

  close(): void {
    this.db.close();
  }

  private migrate(): void {
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS inquiries (
        user_id TEXT NOT NULL,
        id TEXT NOT NULL,
        title TEXT NOT NULL,
        focus TEXT NOT NULL,
        status TEXT NOT NULL CHECK(status IN ('active', 'paused', 'closed')),
        state_json TEXT NOT NULL DEFAULT '{}',
        version INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        PRIMARY KEY (user_id, id)
      );

      CREATE TABLE IF NOT EXISTS inquiry_status_history (
        user_id TEXT NOT NULL,
        inquiry_id TEXT NOT NULL,
        sequence INTEGER NOT NULL,
        changed_at TEXT NOT NULL,
        from_status TEXT,
        to_status TEXT NOT NULL,
        reason TEXT,
        PRIMARY KEY (user_id, inquiry_id, sequence),
        FOREIGN KEY (user_id, inquiry_id)
          REFERENCES inquiries(user_id, id) ON DELETE RESTRICT
      );

      CREATE TABLE IF NOT EXISTS memory_objects (
        user_id TEXT NOT NULL,
        id TEXT NOT NULL,
        title TEXT NOT NULL,
        type TEXT NOT NULL,
        status TEXT NOT NULL,
        content TEXT NOT NULL,
        confidence TEXT,
        source_inquiries_json TEXT NOT NULL DEFAULT '[]',
        tags_json TEXT NOT NULL DEFAULT '[]',
        related_json TEXT NOT NULL DEFAULT '[]',
        supersedes TEXT,
        version INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        PRIMARY KEY (user_id, id)
      );

      CREATE TABLE IF NOT EXISTS idempotency_keys (
        user_id TEXT NOT NULL,
        operation TEXT NOT NULL,
        key TEXT NOT NULL,
        response_json TEXT NOT NULL,
        created_at TEXT NOT NULL,
        PRIMARY KEY (user_id, operation, key)
      );

      CREATE TABLE IF NOT EXISTS audit_log (
        sequence INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        operation TEXT NOT NULL,
        target_id TEXT NOT NULL,
        target_version INTEGER NOT NULL,
        occurred_at TEXT NOT NULL
      );

      CREATE INDEX IF NOT EXISTS inquiries_user_updated
        ON inquiries(user_id, updated_at DESC);
      CREATE INDEX IF NOT EXISTS memory_user_updated
        ON memory_objects(user_id, updated_at DESC);
    `);
  }

  private transaction(action: () => void): void {
    this.db.exec("BEGIN IMMEDIATE");
    try {
      action();
      this.db.exec("COMMIT");
    } catch (error) {
      this.db.exec("ROLLBACK");
      throw error;
    }
  }

  private uniqueId(userId: string, table: "inquiries" | "memory_objects", title: string): string {
    const prefix = `${new Date().toISOString().slice(0, 10)}-${slug(title)}`;
    const statement = this.db.prepare(
      `SELECT 1 FROM ${table} WHERE user_id = ? AND id = ?`,
    );
    let candidate = prefix;
    let suffix = 2;
    while (statement.get(userId, candidate)) candidate = `${prefix}-${suffix++}`;
    return candidate;
  }

  private prior<T>(userId: string, operation: string, key?: string): T | undefined {
    if (!key) return undefined;
    const row = this.db
      .prepare(
        "SELECT response_json FROM idempotency_keys WHERE user_id = ? AND operation = ? AND key = ?",
      )
      .get(userId, operation, key) as { response_json: string } | undefined;
    return row ? parseJson<T>(row.response_json, {} as T) : undefined;
  }

  private remember(userId: string, operation: string, key: string | undefined, result: unknown): void {
    if (!key) return;
    this.db
      .prepare(
        "INSERT INTO idempotency_keys(user_id, operation, key, response_json, created_at) VALUES (?, ?, ?, ?, ?)",
      )
      .run(userId, operation, key, stringify(result), now());
  }

  private audit(userId: string, operation: string, id: string, version: number): void {
    this.db
      .prepare(
        "INSERT INTO audit_log(user_id, operation, target_id, target_version, occurred_at) VALUES (?, ?, ?, ?, ?)",
      )
      .run(userId, operation, id, version, now());
  }

  private inquiryFromRow(row: Record<string, unknown>): InquiryRecord {
    const history = this.db
      .prepare(
        `SELECT changed_at, from_status, to_status, reason
         FROM inquiry_status_history
         WHERE user_id = ? AND inquiry_id = ? ORDER BY sequence`,
      )
      .all(String(row.user_id), String(row.id)) as Array<Record<string, unknown>>;
    return {
      id: String(row.id),
      title: String(row.title),
      focus: String(row.focus),
      status: row.status as InquiryStatus,
      version: Number(row.version),
      created_at: String(row.created_at),
      updated_at: String(row.updated_at),
      state: parseJson<InquiryState>(row.state_json, {}),
      status_history: history.map((item) => ({
        at: String(item.changed_at),
        from: item.from_status ? (String(item.from_status) as InquiryStatus) : null,
        to: String(item.to_status) as InquiryStatus,
        ...(item.reason ? { reason: String(item.reason) } : {}),
      })),
    };
  }

  private memoryFromRow(row: Record<string, unknown>): MemoryRecord {
    return {
      id: String(row.id),
      title: String(row.title),
      type: String(row.type),
      status: String(row.status),
      content: String(row.content),
      ...(row.confidence ? { confidence: String(row.confidence) } : {}),
      source_inquiries: parseJson<string[]>(row.source_inquiries_json, []),
      tags: parseJson<string[]>(row.tags_json, []),
      related: parseJson<string[]>(row.related_json, []),
      ...(row.supersedes ? { supersedes: String(row.supersedes) } : {}),
      version: Number(row.version),
      created_at: String(row.created_at),
      updated_at: String(row.updated_at),
    };
  }

  listInquiries(userId: string, status?: InquiryStatus, limit = 25): InquiryRecord[] {
    const rows = status
      ? this.db
          .prepare(
            "SELECT * FROM inquiries WHERE user_id = ? AND status = ? ORDER BY updated_at DESC LIMIT ?",
          )
          .all(userId, status, limit)
      : this.db
          .prepare("SELECT * FROM inquiries WHERE user_id = ? ORDER BY updated_at DESC LIMIT ?")
          .all(userId, limit);
    return (rows as Array<Record<string, unknown>>).map((row) => this.inquiryFromRow(row));
  }

  getInquiry(userId: string, id: string): InquiryRecord {
    const row = this.db
      .prepare("SELECT * FROM inquiries WHERE user_id = ? AND id = ?")
      .get(userId, id) as Record<string, unknown> | undefined;
    if (!row) throw new NotFoundError(`Inquiry not found: ${id}`);
    return this.inquiryFromRow(row);
  }

  startInquiry(
    userId: string,
    input: { title: string; focus: string; idempotency_key?: string },
  ): InquiryRecord {
    const cached = this.prior<InquiryRecord>(userId, "start_inquiry", input.idempotency_key);
    if (cached) return cached;
    const timestamp = now();
    const id = this.uniqueId(userId, "inquiries", input.title);
    let result: InquiryRecord | undefined;
    this.transaction(() => {
      this.db
        .prepare(
          `INSERT INTO inquiries
           (user_id, id, title, focus, status, state_json, version, created_at, updated_at)
           VALUES (?, ?, ?, ?, 'active', '{}', 1, ?, ?)`,
        )
        .run(userId, id, input.title, input.focus, timestamp, timestamp);
      this.db
        .prepare(
          `INSERT INTO inquiry_status_history
           (user_id, inquiry_id, sequence, changed_at, from_status, to_status)
           VALUES (?, ?, 1, ?, NULL, 'active')`,
        )
        .run(userId, id, timestamp);
      this.audit(userId, "start_inquiry", id, 1);
      result = this.getInquiry(userId, id);
      this.remember(userId, "start_inquiry", input.idempotency_key, result);
    });
    return result!;
  }

  checkpointInquiry(
    userId: string,
    input: {
      id: string;
      expected_version: number;
      summary?: string;
      findings?: string[];
      uncertainty?: string[];
      open_questions?: string[];
      pivots?: string[];
      linked_memory_ids?: string[];
      idempotency_key?: string;
    },
  ): InquiryRecord {
    const cached = this.prior<InquiryRecord>(userId, "checkpoint_inquiry", input.idempotency_key);
    if (cached) return cached;
    const current = this.getInquiry(userId, input.id);
    if (current.version !== input.expected_version) {
      throw new ConflictError(
        `Inquiry ${input.id} is version ${current.version}, not ${input.expected_version}`,
      );
    }
    const state: InquiryState = {
      ...current.state,
      ...(input.summary !== undefined ? { summary: input.summary } : {}),
      ...(input.findings !== undefined ? { findings: input.findings } : {}),
      ...(input.uncertainty !== undefined ? { uncertainty: input.uncertainty } : {}),
      ...(input.open_questions !== undefined ? { open_questions: input.open_questions } : {}),
      ...(input.pivots !== undefined ? { pivots: input.pivots } : {}),
      ...(input.linked_memory_ids !== undefined
        ? { linked_memory_ids: input.linked_memory_ids }
        : {}),
    };
    const version = current.version + 1;
    let updated: InquiryRecord | undefined;
    this.transaction(() => {
      const result = this.db
        .prepare(
          `UPDATE inquiries SET state_json = ?, version = ?, updated_at = ?
           WHERE user_id = ? AND id = ? AND version = ?`,
        )
        .run(stringify(state), version, now(), userId, input.id, input.expected_version);
      if (result.changes !== 1) throw new ConflictError(`Inquiry ${input.id} changed concurrently`);
      this.audit(userId, "checkpoint_inquiry", input.id, version);
      updated = this.getInquiry(userId, input.id);
      this.remember(userId, "checkpoint_inquiry", input.idempotency_key, updated);
    });
    return updated!;
  }

  setInquiryStatus(
    userId: string,
    input: {
      id: string;
      status: InquiryStatus;
      expected_version: number;
      reason?: string;
      idempotency_key?: string;
    },
  ): InquiryRecord {
    const cached = this.prior<InquiryRecord>(userId, "set_inquiry_status", input.idempotency_key);
    if (cached) return cached;
    const current = this.getInquiry(userId, input.id);
    if (current.version !== input.expected_version) {
      throw new ConflictError(
        `Inquiry ${input.id} is version ${current.version}, not ${input.expected_version}`,
      );
    }
    if (current.status === input.status) {
      this.remember(userId, "set_inquiry_status", input.idempotency_key, current);
      return current;
    }
    const version = current.version + 1;
    const timestamp = now();
    this.transaction(() => {
      const update = this.db
        .prepare(
          `UPDATE inquiries SET status = ?, version = ?, updated_at = ?
           WHERE user_id = ? AND id = ? AND version = ?`,
        )
        .run(input.status, version, timestamp, userId, input.id, input.expected_version);
      if (update.changes !== 1) throw new ConflictError(`Inquiry ${input.id} changed concurrently`);
      this.db
        .prepare(
          `INSERT INTO inquiry_status_history
           (user_id, inquiry_id, sequence, changed_at, from_status, to_status, reason)
           SELECT ?, ?, COALESCE(MAX(sequence), 0) + 1, ?, ?, ?, ?
           FROM inquiry_status_history WHERE user_id = ? AND inquiry_id = ?`,
        )
        .run(
          userId,
          input.id,
          timestamp,
          current.status,
          input.status,
          input.reason ?? null,
          userId,
          input.id,
        );
      this.audit(userId, "set_inquiry_status", input.id, version);
      const updated = this.getInquiry(userId, input.id);
      this.remember(userId, "set_inquiry_status", input.idempotency_key, updated);
    });
    return this.getInquiry(userId, input.id);
  }

  saveMemoryObject(
    userId: string,
    input: {
      title: string;
      type: string;
      status: string;
      content: string;
      confidence?: string;
      source_inquiries?: string[];
      tags?: string[];
      related?: string[];
      supersedes?: string;
      idempotency_key?: string;
    },
  ): MemoryRecord {
    const cached = this.prior<MemoryRecord>(userId, "save_memory_object", input.idempotency_key);
    if (cached) return cached;
    const timestamp = now();
    const id = this.uniqueId(userId, "memory_objects", input.title);
    let result: MemoryRecord | undefined;
    this.transaction(() => {
      this.db
        .prepare(
          `INSERT INTO memory_objects
           (user_id, id, title, type, status, content, confidence, source_inquiries_json,
            tags_json, related_json, supersedes, version, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)`,
        )
        .run(
          userId,
          id,
          input.title,
          input.type,
          input.status,
          input.content,
          input.confidence ?? null,
          stringify(input.source_inquiries ?? []),
          stringify(input.tags ?? []),
          stringify(input.related ?? []),
          input.supersedes ?? null,
          timestamp,
          timestamp,
        );
      this.audit(userId, "save_memory_object", id, 1);
      result = this.getMemoryObject(userId, id);
      this.remember(userId, "save_memory_object", input.idempotency_key, result);
    });
    return result!;
  }

  getMemoryObject(userId: string, id: string): MemoryRecord {
    const row = this.db
      .prepare("SELECT * FROM memory_objects WHERE user_id = ? AND id = ?")
      .get(userId, id) as Record<string, unknown> | undefined;
    if (!row) throw new NotFoundError(`Memory object not found: ${id}`);
    return this.memoryFromRow(row);
  }

  searchMemory(userId: string, query: string, limit = 10): MemoryRecord[] {
    const pattern = `%${query.replace(/[\\%_]/g, "\\$&")}%`;
    const rows = this.db
      .prepare(
        `SELECT * FROM memory_objects
         WHERE user_id = ? AND (
           title LIKE ? ESCAPE '\\' OR content LIKE ? ESCAPE '\\' OR tags_json LIKE ? ESCAPE '\\'
         ) ORDER BY updated_at DESC LIMIT ?`,
      )
      .all(userId, pattern, pattern, pattern, limit) as Array<Record<string, unknown>>;
    return rows.map((row) => this.memoryFromRow(row));
  }

  updateMemoryMetadata(
    userId: string,
    input: {
      id: string;
      expected_version: number;
      title?: string;
      type?: string;
      status?: string;
      confidence?: string | null;
      tags?: string[];
      related?: string[];
      supersedes?: string | null;
      idempotency_key?: string;
    },
  ): MemoryRecord {
    const cached = this.prior<MemoryRecord>(userId, "update_memory_metadata", input.idempotency_key);
    if (cached) return cached;
    const current = this.getMemoryObject(userId, input.id);
    if (current.version !== input.expected_version) {
      throw new ConflictError(
        `Memory object ${input.id} is version ${current.version}, not ${input.expected_version}`,
      );
    }
    const version = current.version + 1;
    let updated: MemoryRecord | undefined;
    this.transaction(() => {
      const result = this.db
        .prepare(
          `UPDATE memory_objects SET
             title = ?, type = ?, status = ?, confidence = ?, tags_json = ?, related_json = ?,
             supersedes = ?, version = ?, updated_at = ?
           WHERE user_id = ? AND id = ? AND version = ?`,
        )
        .run(
          input.title ?? current.title,
          input.type ?? current.type,
          input.status ?? current.status,
          input.confidence === undefined ? (current.confidence ?? null) : input.confidence,
          stringify(input.tags ?? current.tags),
          stringify(input.related ?? current.related),
          input.supersedes === undefined ? (current.supersedes ?? null) : input.supersedes,
          version,
          now(),
          userId,
          input.id,
          input.expected_version,
        );
      if (result.changes !== 1) {
        throw new ConflictError(`Memory object ${input.id} changed concurrently`);
      }
      this.audit(userId, "update_memory_metadata", input.id, version);
      updated = this.getMemoryObject(userId, input.id);
      this.remember(userId, "update_memory_metadata", input.idempotency_key, updated);
    });
    return updated!;
  }
}
