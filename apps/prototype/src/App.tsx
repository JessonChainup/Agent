import { useState } from "react";
import "./App.css";

export default function App() {
  const [step, setStep] = useState<"idle" | "confirm">("idle");

  const specHref =
    "https://github.com/JessonChainup/Agent/blob/main/docs/REQ-STAFFONEWS-KICKOFF/20-spec/spec.md";

  return (
    <main className="shell">
      <h1>原型占位页 · REQ-STAFFONEWS-KICKOFF</h1>
      <p className="lede">
        试点：**交付方法论 + Gate** 对齐 GitHub · 当前 SPEC 可读入口：
        <a href={specHref} target="_blank" rel="noreferrer noopener">
          打开 GitHub Spec
        </a>
        。编排见仓库 <code>docs/</code> 与 <code>references/product-delivery/ORCHESTRATION.md</code>（Hermes MCP）。
      </p>
      <p>
        替换为本 REQ 的核心交互（路由 / 表单 / 状态机）。文档见仓库{" "}
        <code>docs/&lt;REQ-ID&gt;/</code>。
      </p>
      <div className="card">
        <p>示例交互：当前步骤 —— {step}</p>
        <button type="button" onClick={() => setStep(step === "idle" ? "confirm" : "idle")}>
          切换状态
        </button>
      </div>
    </main>
  );
}
