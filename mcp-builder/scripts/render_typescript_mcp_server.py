#!/usr/bin/env python3
"""Render a minimal TypeScript MCP server skeleton."""

from __future__ import annotations

import argparse
from pathlib import Path
from textwrap import dedent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a minimal TypeScript MCP server skeleton for MCP projects.",
    )
    parser.add_argument("--server-name", required=True, help="MCP server name")
    parser.add_argument("--version", default="0.1.0", help="Server version")
    parser.add_argument("--tool-name", default="search_items", help="Example tool name")
    parser.add_argument("--output", required=True, help="Output TypeScript file path")
    return parser.parse_args()


def sanitize_identifier(value: str) -> str:
    chars = []
    upper_next = True
    for ch in value:
      if ch.isalnum():
          chars.append(ch.upper() if upper_next else ch)
          upper_next = False
      else:
          upper_next = True
    result = "".join(chars) or "GeneratedTool"
    if result[0].isdigit():
        result = f"Tool{result}"
    return result


def render(server_name: str, version: str, tool_name: str) -> str:
    schema_name = f"{sanitize_identifier(tool_name)}Input"
    return dedent(
        f'''\
        import {{ McpServer }} from "@modelcontextprotocol/sdk/server/mcp.js";
        import {{ StdioServerTransport }} from "@modelcontextprotocol/sdk/server/stdio.js";
        import {{ z }} from "zod";

        const server = new McpServer({{
          name: "{server_name}",
          version: "{version}",
        }});

        const {schema_name} = {{
          query: z.string().min(1).describe("Search keyword"),
          limit: z.number().int().min(1).max(50).default(10).describe("Maximum items to return"),
        }};

        server.tool(
          "{tool_name}",
          {schema_name},
          async ({{ query, limit = 10 }}) => {{
            try {{
              const items = await fakeSearch(query, limit);

              return {{
                content: [
                  {{
                    type: "text",
                    text: JSON.stringify(
                      {{
                        summary: `Found ${{items.length}} items`,
                        items,
                      }},
                      null,
                      2,
                    ),
                  }},
                ],
              }};
            }} catch (error) {{
              const message = error instanceof Error ? error.message : "Unknown error";
              throw new Error("{tool_name} failed: " + message);
            }}
          }},
        );

        async function fakeSearch(query: string, limit: number) {{
          return Array.from({{ length: limit }}).map((_, index) => ({{
            id: `item_${{index + 1}}`,
            name: `${{query}}-${{index + 1}}`,
          }}));
        }}

        const transport = new StdioServerTransport();
        await server.connect(transport);
        '''
    )


def main() -> None:
    args = parse_args()
    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render(args.server_name, args.version, args.tool_name),
        encoding="utf-8",
    )
    print(output_path)


if __name__ == "__main__":
    main()
