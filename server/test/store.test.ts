import assert from "node:assert/strict";
import { test } from "node:test";

import { ConflictError, DialecticalStore, NotFoundError } from "../src/store.js";

test("inquiry lifecycle preserves versions, history, and user isolation", () => {
  const store = new DialecticalStore(":memory:");
  try {
    const created = store.startInquiry("alice", {
      title: "Pricing strategy",
      focus: "Understand whether a price change caused churn.",
      idempotency_key: "start-1",
    });
    const replay = store.startInquiry("alice", {
      title: "Ignored on replay",
      focus: "Ignored on replay",
      idempotency_key: "start-1",
    });
    assert.equal(replay.id, created.id);
    assert.equal(created.version, 1);
    assert.equal(created.status_history.length, 1);

    const checkpoint = store.checkpointInquiry("alice", {
      id: created.id,
      expected_version: 1,
      summary: "Churn rose after the price change, but causality is unresolved.",
      findings: ["Timing is consistent with the price-change hypothesis."],
      uncertainty: ["A product redesign shipped during the same week."],
      open_questions: ["Did treated and untreated cohorts differ before launch?"],
      pivots: ["Moved from a single-cause story to competing hypotheses."],
      linked_memory_ids: ["2026-10-04-pricing-and-churn"],
    });
    assert.equal(checkpoint.version, 2);
    assert.equal(checkpoint.state.uncertainty?.length, 1);
    assert.equal(checkpoint.state.pivots?.length, 1);

    assert.throws(
      () =>
        store.checkpointInquiry("alice", {
          id: created.id,
          expected_version: 1,
          summary: "Stale update",
        }),
      ConflictError,
    );

    const closed = store.setInquiryStatus("alice", {
      id: created.id,
      status: "closed",
      expected_version: 2,
      reason: "Investigation complete; causal claim remains qualified.",
    });
    assert.equal(closed.status, "closed");
    assert.equal(closed.version, 3);
    assert.deepEqual(
      closed.status_history.map(({ from, to }) => [from, to]),
      [
        [null, "active"],
        ["active", "closed"],
      ],
    );
    assert.throws(() => store.getInquiry("bob", created.id), NotFoundError);
  } finally {
    store.close();
  }
});

test("memory objects remain scoped, searchable, and content-stable during tagging", () => {
  const store = new DialecticalStore(":memory:");
  try {
    const saved = store.saveMemoryObject("alice", {
      title: "Pricing and churn",
      type: "finding",
      status: "developing",
      content: "The timing fits, but a concurrent redesign remains a live alternative.",
      confidence: "moderate",
      source_inquiries: ["2026-10-04-pricing-strategy"],
      tags: ["pricing"],
      idempotency_key: "save-1",
    });
    assert.equal(store.searchMemory("alice", "redesign")[0]?.id, saved.id);
    assert.equal(store.searchMemory("bob", "redesign").length, 0);

    const tagged = store.updateMemoryMetadata("alice", {
      id: saved.id,
      expected_version: 1,
      tags: ["pricing", "churn"],
      related: ["2026-10-04-experiment-design"],
    });
    assert.equal(tagged.version, 2);
    assert.equal(tagged.content, saved.content);
    assert.deepEqual(tagged.tags, ["pricing", "churn"]);
  } finally {
    store.close();
  }
});
