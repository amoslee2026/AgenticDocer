import { useMemo } from "react";
import { marked } from "marked";
import { toAssetUrl } from "../api/client";

/**
 * 渲染正文视图（M04 markdown 直通展示）。
 * 资产重写在 DOM 层做：md 图片与 HTML `<img>` 两种形态（A7）统一命中
 * `assets/<sha256>.<ext>` → `/api/v1/assets/<sha256>`；其余原样。
 */
export function MarkdownView({ markdown }: { markdown: string }) {
  const html = useMemo(() => {
    const container = document.createElement("div");
    const raw = marked.parse(markdown, { async: false }) as string;
    for (const img of Array.from(container.querySelectorAll("img"))) {
      const src = img.getAttribute("src") ?? "";
      img.setAttribute("src", toAssetUrl(src));
    }
    return container.innerHTML;
  }, [markdown]);
  return <div className="doc-body" dangerouslySetInnerHTML={{ __html: html }} />;
}
