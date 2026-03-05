// =============================================================
// Google Apps Script — paste this into your Sheet's script editor
// (Extensions > Apps Script)
//
// After pasting:
//   1. Click Deploy > New deployment
//   2. Type: Web app
//   3. Execute as: Me
//   4. Who has access: Anyone
//   5. Click Deploy, authorize, copy the URL
//   6. Save the URL in your .env as SHEETS_WEBHOOK_URL
// =============================================================

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(30000);

  try {
    var payload = JSON.parse(e.postData.contents);
    var ss = SpreadsheetApp.getActiveSpreadsheet();

    if (payload.kanban) {
      writeKanban(ss, payload.kanban);
    }
    if (payload.daily_log) {
      writeDailyLog(ss, payload.daily_log);
    }
    if (payload.this_week) {
      writeThisWeek(ss, payload.this_week);
    }
    if (payload.daily_metrics) {
      writeDailyMetrics(ss, payload.daily_metrics);
    }

    return ContentService
      .createTextOutput(JSON.stringify({ status: "ok" }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: "error", message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}

// -- Kanban tab: three-column board (Backlog | Doing | Done) -----------
function writeKanban(ss, rows) {
  var sheet = ss.getSheetByName("Kanban");
  if (!sheet) {
    sheet = ss.insertSheet("Kanban");
  }
  sheet.clearContents();

  // Organize tasks by status
  var backlog = [];
  var doing = [];
  var done = [];

  rows.forEach(function(r) {
    var taskLine = "[" + r.board + "] " + r.task;
    if (r.status === "To Do") {
      backlog.push(taskLine);
    } else if (r.status === "Doing") {
      doing.push(taskLine);
    } else if (r.status === "Done") {
      done.push(taskLine);
    }
  });

  // Headers
  var headers = ["Backlog", "Doing", "Done"];
  sheet.getRange(1, 1, 1, 3).setValues([headers]);
  sheet.getRange(1, 1, 1, 3).setFontWeight("bold");
  sheet.getRange(1, 1, 1, 3).setBackground("#d9d9d9");

  // Find max column height
  var maxRows = Math.max(backlog.length, doing.length, done.length);

  // Write tasks in rows, padding with empty strings
  for (var i = 0; i < maxRows; i++) {
    var row = [
      backlog[i] || "",
      doing[i] || "",
      done[i] || ""
    ];
    sheet.getRange(i + 2, 1, 1, 3).setValues([row]);
  }

  // Auto-fit column widths
  sheet.autoResizeColumns(1, 3);
}

// -- Daily Log tab: append (never clear) ----------------------
function writeDailyLog(ss, entry) {
  var sheet = ss.getSheetByName("Daily Log");
  if (!sheet) {
    sheet = ss.insertSheet("Daily Log");
  }

  var headers = ["Date", "Intentions", "Work Completed", "Commits"];

  // Write header if sheet is empty
  if (sheet.getLastRow() === 0) {
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
    sheet.getRange(1, 1, 1, headers.length).setFontWeight("bold");
  }

  // Check if today already has a row — update it instead of appending
  var lastRow = sheet.getLastRow();
  var existingRow = -1;
  if (lastRow > 1) {
    var dates = sheet.getRange(2, 1, lastRow - 1, 1).getValues();
    for (var i = 0; i < dates.length; i++) {
      if (dates[i][0] === entry.date) {
        existingRow = i + 2; // 1-indexed, skip header
        break;
      }
    }
  }

  var row = [
    entry.date,
    entry.intentions || "",
    entry.work_completed || "",
    entry.commits || ""
  ];

  if (existingRow > 0) {
    sheet.getRange(existingRow, 1, 1, headers.length).setValues([row]);
  } else {
    sheet.appendRow(row);
  }
}

// -- This Week tab: snapshot replace --------------------------
function writeThisWeek(ss, rows) {
  var sheet = ss.getSheetByName("This Week");
  if (!sheet) {
    sheet = ss.insertSheet("This Week");
  }
  sheet.clearContents();

  var headers = ["Task", "Board", "Status", "Notes"];
  var data = [headers];
  rows.forEach(function(r) {
    data.push([r.task, r.board, r.status, r.notes || ""]);
  });
  if (data.length > 1) {
    sheet.getRange(1, 1, data.length, headers.length).setValues(data);
  } else {
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  }

  sheet.getRange(1, 1, 1, headers.length).setFontWeight("bold");
}

// -- Daily Metrics tab: snapshot replace --------------------------
function writeDailyMetrics(ss, metrics) {
  var sheet = ss.getSheetByName("Daily Metrics");
  if (!sheet) {
    sheet = ss.insertSheet("Daily Metrics");
  }
  sheet.clearContents();

  var headers = ["Date", "To Do", "Doing", "Done", "Total Tasks", "Completion %"];
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  sheet.getRange(1, 1, 1, headers.length).setFontWeight("bold");
  sheet.getRange(1, 1, 1, headers.length).setBackground("#d9d9d9");

  var row = [
    metrics.date,
    metrics.to_do,
    metrics.doing,
    metrics.done,
    metrics.total,
    metrics.completion_pct
  ];

  sheet.getRange(2, 1, 1, headers.length).setValues([row]);

  // Color code completion ratio
  var completionCell = sheet.getRange(2, 6);
  if (metrics.completion_ratio >= 75) {
    completionCell.setBackground("#c6efce"); // Green: 75%+ done
  } else if (metrics.completion_ratio >= 50) {
    completionCell.setBackground("#fff2cc"); // Yellow: 50-75% done
  } else {
    completionCell.setBackground("#ffcccc"); // Red: <50% done
  }

  // Auto-fit columns
  sheet.autoResizeColumns(1, headers.length);
}

// -- Test function (run manually to verify) -------------------
function testDoPost() {
  var payload = {
    kanban: [
      { board: "today", task: "Test task", status: "To Do", updated: "2026-03-02" }
    ],
    daily_log: {
      date: "2026-03-02",
      intentions: "Test the sync pipeline",
      work_completed: "Created Apps Script webhook",
      commits: "abc1234"
    },
    this_week: [
      { task: "Test task", board: "this_week", status: "To Do", notes: "" }
    ]
  };

  var e = { postData: { contents: JSON.stringify(payload) } };
  var result = doPost(e);
  Logger.log(result.getContent());
}
