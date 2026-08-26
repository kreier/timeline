/**
 * Cloudflare Worker: Dictionary Translation Submission Proxy
 * Environment Secrets / Variables required in Cloudflare Dashboard:
 * - GITHUB_TOKEN: Personal Access Token (with 'repo' scope) or GitHub App Token
 * - GITHUB_REPO: "kreier/timeline"
 * - TURNSTILE_SECRET_KEY: (Optional/Recommended) Secret key from Cloudflare Turnstile
 */

export default {
  async fetch(request, env) {
    // Handle CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type"
        }
      });
    }

    if (request.method !== "POST") {
      return new Response(JSON.stringify({ error: "Method not allowed" }), {
        status: 405,
        headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
      });
    }

    try {
      const payload = await request.json();
      const { lang, editor, date, changes, turnstileToken } = payload;

      if (!lang || !editor || !changes || !Array.isArray(changes) || changes.length === 0) {
        return new Response(JSON.stringify({ error: "Invalid submission payload" }), {
          status: 400,
          headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
        });
      }

      // 1. Optional Turnstile validation
      if (env.TURNSTILE_SECRET_KEY && turnstileToken && turnstileToken !== "mock-or-turnstile-token") {
        const turnstileRes = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: new URLSearchParams({
            secret: env.TURNSTILE_SECRET_KEY,
            response: turnstileToken
          })
        });
        const turnstileOutcome = await turnstileRes.json();
        if (!turnstileOutcome.success) {
          return new Response(JSON.stringify({ error: "Bot verification failed" }), {
            status: 403,
            headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
          });
        }
      }

      // 2. Build human-readable markdown body
      let markdownBody = `### 📝 Proposed Translation Updates\n\n`;
      markdownBody += `- **Language:** \`${lang.toUpperCase()}\`\n`;
      markdownBody += `- **Editor:** ${editor}\n`;
      markdownBody += `- **Date:** ${date || new Date().toISOString().split("T")[0]}\n`;
      markdownBody += `- **Total Entries:** ${changes.length}\n\n`;
      markdownBody += `| Key | Category | Field | Original Value | Proposed Value |\n`;
      markdownBody += `| :--- | :--- | :--- | :--- | :--- |\n`;

      for (const item of changes) {
        if (item.text !== item.origText) {
          markdownBody += `| \`${item.key}\` | ${item.category} | **Text** | ${escapePipe(item.origText)} | **${escapePipe(item.text)}** |\n`;
        }
        if (item.notes !== item.origNotes) {
          markdownBody += `| \`${item.key}\` | ${item.category} | **Notes** | ${escapePipe(item.origNotes || "-")} | **${escapePipe(item.notes || "-")}** |\n`;
        }
        if (item.checked !== item.origChecked) {
          markdownBody += `| \`${item.key}\` | ${item.category} | **Checked** | ${item.origChecked === "True" ? "✅" : "⬜"} | **${item.checked === "True" ? "✅" : "⬜"}** |\n`;
        }
      }

      markdownBody += `\n---\n#### 🤖 Machine Payload\n<!-- SUBMISSION_JSON_START -->\n\`\`\`json\n`;
      markdownBody += JSON.stringify(payload, null, 2);
      markdownBody += `\n\`\`\`\n<!-- SUBMISSION_JSON_END -->\n\n`;
      markdownBody += `> Maintainer command: Reply with \`/approve\` to apply these changes directly to \`db/dictionary_${lang}.csv\`.`;

      // 3. Create GitHub Issue
      const repo = env.GITHUB_REPO || "kreier/timeline";
      const keyListSummary = changes.map(c => c.key).slice(0, 3).join(", ") + (changes.length > 3 ? "..." : "");
      const issueTitle = `[Update Translation] ${lang.toUpperCase()}: ${keyListSummary} (by ${editor})`;

      const ghResponse = await fetch(`https://api.github.com/repos/${repo}/issues`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${env.GITHUB_TOKEN}`,
          "User-Agent": "Dictionary-Submission-Worker",
          "Accept": "application/vnd.github.v3+json",
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          title: issueTitle,
          body: markdownBody,
          labels: ["update-dictionary", `lang:${lang}`]
        })
      });

      if (!ghResponse.ok) {
        const ghError = await ghResponse.text();
        return new Response(JSON.stringify({ error: "Failed to create GitHub issue", details: ghError }), {
          status: 502,
          headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
        });
      }

      const issueData = await ghResponse.json();

      return new Response(JSON.stringify({
        success: true,
        issue_number: issueData.number,
        issue_url: issueData.html_url
      }), {
        status: 200,
        headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
      });

    } catch (err) {
      return new Response(JSON.stringify({ error: err.message }), {
        status: 500,
        headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
      });
    }
  }
};

function escapePipe(str) {
  if (!str) return "";
  return str.replace(/\|/g, "\\|").replace(/\n/g, "<br>");
}
