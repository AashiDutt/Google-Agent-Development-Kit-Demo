# Python for Node.js Developers

A quick reference to the Python patterns used in this codebase, translated for a Node.js developer.

---

## Project Structure

```
agents/host_agent/       → package (like a module/npm package)
  ├── __init__.py        → marks directory as importable (empty or setup)
  ├── __main__.py        → entry point (like bin/ or index.js with exports)
  ├── agent.py           → ADK agent definition + execute()
  ├── task_manager.py    → wraps agent for HTTP (like a controller)
  └── .well-known/       → ADK discovery metadata
common/                  → shared code (like a shared lib)
  ├── a2a_client.py      → HTTP client for agent-to-agent calls
  └── a2a_server.py      → FastAPI server factory
shared/
  └── schemas.py         → Pydantic models (like zod/types)
requirements.txt         → package.json (dependencies)
```

---

## Imports (vs Node.js)

| Python                          | Node.js equivalent                    |
|----------------------------------|----------------------------------------|
| `import httpx`                  | `const httpx = require('httpx')`      |
| `from http.client import run`   | `const { run } = require('http/client')` |
| `from .agent import execute`    | `const { execute } = require('./agent')` |
| `from ..common import a2a`      | `const { a2a } = require('../common')` |

**`.` means "same directory"** — `from .agent import execute` in `task_manager.py` imports `agent.py` in the same folder. Without the dot, Python looks at the project root, not the current package.

---

## `__main__.py` — Entry Point

Like `bin/` or `index.js` with `#!/usr/bin/env node`. When you run:

```sh
uvicorn agents.flight_agent.__main__:app
```

Python executes `agents/flight_agent/__main__.py` and looks for a variable called `app`.

The `if __name__ == "__main__":` guard is like `if (require.main === module)` — code only runs when the file is executed directly, not when imported:

```python
if __name__ == "__main__":    # if require.main === module
    import uvicorn
    uvicorn.run(app, port=8001)
```

---

## Imports in `__init__.py`

`__init__.py` marks a directory as a Python package. Empty file = "this is a package". Without it, `from .agent import execute` won't work. No direct JS equivalent — closest is having an `index.js` that re-exports.

---

## `async` / `await`

Same as Node.js. Mark functions with `async def` instead of `async function`:

```python
# Python                             # Node.js
async def run(payload):              async function run(payload) {
    result = await execute(payload)      const result = await execute(payload)
    return {"data": result}              return { data: result }
```

---

## Type Hints (vs TypeScript)

Python has optional type hints — they're not enforced at runtime (like TypeScript's `noEmit`):

```python
async def call_agent(url: str, payload: dict) -> dict:    # : str is like TS, -> dict is return type
    ...
```

But there's no TypeScript compiler checking them. They're for IDE support and documentation only unless you run `mypy`.

---

## Pydantic `BaseModel` (like zod / io-ts)

```python
from pydantic import BaseModel

class TravelRequest(BaseModel):
    destination: str
    start_date: str
    end_date: str
    budget: float
```

Equivalent zod:
```typescript
const TravelRequest = z.object({
  destination: z.string(),
  start_date: z.string(),
  end_date: z.string(),
  budget: z.number(),
});
```

`BaseModel` auto-validates data and gives you `.dict()` and `.json()` methods.

---

## FastAPI (like Express.js)

```python
app = FastAPI()                       # const app = express()

@app.post("/run")                     # app.post("/run", async (req, res) => { ... })
async def run(payload: dict):
    return await agent.execute(payload)  # res.json() is automatic
```

Key difference: FastAPI **automatically** parses JSON body into `payload` (no `body-parser` needed) and serializes the return value to JSON (no `res.json()` needed).

---

## Uvicorn (like `node index.js`)

Uvicorn is an ASGI server — it takes a FastAPI app and makes it listen on a port:

```sh
uvicorn agents.flight_agent.__main__:app --host 0.0.0.0 --port 8001
#        package.module.file     :variable  --all interfaces   --port
```

In Node.js you'd do `app.listen(8001)` — in Python you use a separate server process.

---

## `type("Agent", (), {"execute": run})` — Dynamic Class

```python
type("Agent", (), {"execute": run})
```

This creates a class on the fly. Equivalent to:

```python
class Agent:
    execute = run        # run is a function
```

And equivalent to this in Node.js:

```javascript
const Agent = { execute: run };    // just an object with a method
```

It's used to wrap a function into an object so `create_app` can call `agent.execute(payload)` uniformly. In Node.js, you'd just pass the function directly or use `{ run }`.

---

## `dict.get(key, default)` — Safe Access

```python
flights.get("flights", "No flights returned.")
```

Like optional chaining + nullish coalescing in JS:

```javascript
flights?.flights ?? "No flights returned."
```

`dict[key]` throws `KeyError` if key is missing (like JS throwing on `undefined` access). `dict.get(key, default)` is the safe version.

---

## Context Managers (`async with`)

```python
async with httpx.AsyncClient() as client:   # like using (C#) / try-with-resources (Java)
    response = await client.post(...)
```

Equivalent to:
```javascript
const client = new httpx.AsyncClient();
try {
  const response = await client.post(...);
} finally {
  await client.close();
}
```

The `async with` block auto-closes the client when the block exits.

---

## Generator / `async for` (like `for await...of`)

```python
async for event in runner.run_async(...):     # for await (const event of runner.runAsync()) {
    if event.is_final_response():
        return event.content.parts[0].text
```

Python's `async for` is identical to JS `for await...of` — iterates over an async generator, yielding values as they arrive (streaming).

---

## `requirements.txt` (like `package.json`)

```txt
google-adk
fastapi
uvicorn
httpx
pydantic
```

Each line is a package name. No version ranges (bad practice, but works). Install with:

```sh
pip install -r requirements.txt   # like npm install
```

No lockfile by default (unlike `package-lock.json`). Pin versions with `package==1.2.3`.

---

## Virtual Environments (like `.nvmrc` + `node_modules`)

```sh
python3 -m venv adk_demo          # create env (like nvm use + mkdir node_modules)
source adk_demo/bin/activate      # activate (like nvm use)
pip install -r requirements.txt   # npm install
deactivate                        # deactivate
```

Python doesn't auto-isolate dependencies per project — you manually create a venv. Without one, `pip install` goes global (like `npm i -g`).

---

## Common Gotchas for Node.js Devs

| Node.js | Python | Gotcha |
|---------|--------|--------|
| `null` | `None` | Different keyword |
| `undefined` | Not a thing | Attr access on missing key throws `KeyError` |
| `true/false` | `True/False` | Capitalized |
| `&& \|\|` | `and / or` | Words, not symbols |
| `'string' + 5` | `str(5)` | `'string' + 5` throws `TypeError` |
| `{...spread}` | `{**dict}` | `**` unpacks dicts |
| `forEach/map` | List comprehensions | `[x*2 for x in items]` |
| `const`, `let` | Just `variable =` | No const — naming convention: `UPPER = "constant"` |
| `// comment` | `# comment` | `#` not `//` |
| Semicolons optional | No semicolons | Blank line is significant (block separator) |

---

## Quick Cheat Sheet

```python
# Variable
name = "hello"              # const name = "hello"

# List (array)
items = [1, 2, 3]           # const items = [1, 2, 3]
items[0]                    # items[0]
items.append(4)             # items.push(4)

# Dict (object)
d = {"key": "value"}        # const d = { key: "value" }
d["key"]                    # d.key
d.get("key", "default")     # d?.key ?? "default"

# If/else
if x > 5:                   # if (x > 5) {
    do_thing()              #   doThing()
else:                       # } else {
    other()                 #   other()
                            # }

# For loop
for item in items:          # for (const item of items) {
    print(item)             #   console.log(item)
                            # }

# F-strings (template literals)
f"Hello {name}"             # `Hello ${name}`

# Ternary
"yes" if x > 5 else "no"    # x > 5 ? "yes" : "no"
```
