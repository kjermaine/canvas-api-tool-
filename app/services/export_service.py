class ExportService:
    def modules_to_markdown(self, course_ref, modules: list[dict]) -> str:
        lines = [f"# Modules for {course_ref}", ""]

        for module in modules:
            lines.append(f"## {module.get('name', 'Untitled Module')}")
            lines.append("")
            lines.append(f"- ID: {module.get('id')}")
            lines.append(f"- Published: {module.get('published')}")
            lines.append("")

            items = module.get("items") or []
            if items:
                lines.append("### Items")
                for item in items:
                    title = item.get("title", "Untitled Item")
                    item_type = item.get("type", "unknown")
                    html_url = item.get("html_url", "")
                    if html_url:
                        lines.append(f"- [{title}]({html_url}) — `{item_type}`")
                    else:
                        lines.append(f"- {title} — `{item_type}`")
                lines.append("")

        return "\n".join(lines)