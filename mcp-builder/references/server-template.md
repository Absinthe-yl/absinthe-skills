# TypeScript MCP Server Template

这个参考文件提供从零起步时的推荐骨架。默认基线：TypeScript、`@modelcontextprotocol/sdk`、`zod`、`stdio` transport。

## Recommended Files

```text
my-mcp-server/
├── package.json
├── tsconfig.json
├── src/
│   └── index.ts
└── test/
    └── smoke.test.ts
```

## package.json

```json
{
  "name": "my-mcp-server",
  "version": "0.1.0",
  "type": "module",
  "private": true,
  "scripts": {
    "build": "tsc -p tsconfig.json",
    "dev": "tsx src/index.ts",
    "start": "node dist/index.js",
    "test": "vitest run"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.13.0",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "tsx": "^4.19.2",
    "typescript": "^5.6.3",
    "vitest": "^2.1.8"
  }
}
```

## src/index.ts

```ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "my-mcp-server",
  version: "0.1.0",
});

const SearchItemsInput = {
  query: z.string().min(1).describe("Search keyword"),
  limit: z.number().int().min(1).max(50).default(10).describe("Maximum items to return"),
};

server.tool(
  "search_items",
  SearchItemsInput,
  async ({ query, limit = 10 }) => {
    try {
      const items = await fakeSearch(query, limit);

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(
              {
                summary: `Found ${items.length} items`,
                items,
              },
              null,
              2,
            ),
          },
        ],
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unknown error";
      throw new Error(`search_items failed: ${message}`);
    }
  },
);

async function fakeSearch(query: string, limit: number) {
  return Array.from({ length: limit }).map((_, index) => ({
    id: `item_${index + 1}`,
    name: `${query}-${index + 1}`,
  }));
}

const transport = new StdioServerTransport();
await server.connect(transport);
```

## Basic Resource Pattern

如果需要暴露大块只读上下文，可增加 resource：

```ts
server.resource(
  "schema://orders",
  "schema://orders",
  async () => ({
    contents: [
      {
        uri: "schema://orders",
        text: JSON.stringify(
          {
            table: "orders",
            fields: ["id", "customer_id", "status", "created_at"],
          },
          null,
          2,
        ),
      },
    ],
  }),
);
```

## Config Pattern

推荐把凭证和基础配置收口到一个函数：

```ts
function getRequiredEnv(name: string) {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing environment variable: ${name}`);
  }
  return value;
}

const apiBaseUrl = process.env.API_BASE_URL ?? "https://api.example.com";
const apiToken = getRequiredEnv("API_TOKEN");
```

## Test Starting Point

```ts
import { describe, expect, it } from "vitest";

describe("smoke", () => {
  it("loads the module", async () => {
    const mod = await import("../src/index.ts");
    expect(mod).toBeDefined();
  });
});
```

## Delivery Reminder

最终交付时，至少补齐：

- `.env.example` 或环境变量清单
- `README.md` 里的安装与运行步骤
- 一条最小调用示例
- 一条失败路径说明

不要把这份模板原封不动扔给用户；要替换成当前项目的真实工具名、真实 schema 和真实数据访问逻辑。
