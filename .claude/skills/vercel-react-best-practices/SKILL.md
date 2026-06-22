---
name: vercel-react-best-practices
description: 中文 React 与 Next.js 性能优化 Skill。编写、审查或重构 React 组件、Next.js 页面、Server Components、数据请求、Bundle 和交互逻辑时调用，优先消除请求瀑布、缩小包体积并减少无效渲染。
license: MIT
metadata:
  title_zh: Vercel React 与 Next.js 最佳实践
  language: zh-CN
  author: vercel
  source_project: vercel-labs/agent-skills
  source_url: https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices
  version: "1.0.0-zh"
---

# Vercel React 与 Next.js 最佳实践

面向 React 和 Next.js 项目的性能开发与代码审查工作流。按影响程度处理问题：先解决请求瀑布和包体积，再处理服务端、客户端请求、重复渲染与 JavaScript 微优化。

## 何时调用

- 新建 React 组件或 Next.js 页面。
- 编写 Server Component、Server Action、Route Handler 或 API Route。
- 实现客户端或服务端数据获取。
- 页面首屏慢、交互卡顿、Bundle 过大或重复渲染。
- 审查、重构或优化已有 React/Next.js 代码。

## 优先级

| 优先级 | 类别 | 影响 |
|---:|---|---|
| 1 | 消除异步瀑布 | 严重 |
| 2 | 缩小 Bundle | 严重 |
| 3 | 服务端性能 | 高 |
| 4 | 客户端数据请求 | 中高 |
| 5 | 减少重复渲染 | 中 |
| 6 | 渲染性能 | 中 |
| 7 | JavaScript 性能 | 中低 |
| 8 | 高级模式 | 低 |

## 1. 消除异步瀑布

- 只在真正需要的分支中执行 `await`。
- 独立请求使用 `Promise.all()` 并行启动。
- 有部分依赖时先创建 Promise，再组合等待，避免无关任务串行。
- API Route 和 Server Action 中采用“尽早启动，尽晚等待”。
- 用合理的 `Suspense` 边界流式显示页面，不要让整个外壳等待最慢数据。
- 异步条件与廉价同步条件并存时，先检查同步条件。

```ts
// 不推荐：三个往返串行
const user = await fetchUser()
const posts = await fetchPosts()
const config = await fetchConfig()

// 推荐：独立任务并行
const [user, posts, config] = await Promise.all([
  fetchUser(),
  fetchPosts(),
  fetchConfig(),
])
```

## 2. 缩小 Bundle

- 避免从大型 barrel 文件统一导入，直接导入实际模块。
- 重型组件使用 `next/dynamic` 或按需加载。
- 分析、日志、客服等非首屏第三方库在 hydration 后加载。
- 功能未启用时不要加载对应模块。
- 对高概率后续访问的资源，在 hover、focus 或明确意图出现时预加载。
- 使用静态可分析的导入路径，避免运行时拼接路径扩大打包范围。

## 3. 服务端性能

- Server Action 必须像 API 一样做鉴权和输入验证。
- 使用 `React.cache()` 做单次请求内去重。
- 跨请求缓存使用有上限的 LRU 或框架缓存，禁止无限增长的全局 Map。
- 不要在模块级共享可变的用户或请求状态。
- 减少从 Server Component 传给 Client Component 的序列化数据。
- 静态字体、图标和配置读取可提升到模块级。
- 重构组件边界，让互不依赖的数据并行获取。
- 非阻塞日志和统计任务放到响应完成后执行。

## 4. 客户端数据请求

- 对重复请求使用 SWR、React Query 或等价去重机制。
- 全局事件监听器只能注册一次，并在卸载时清理。
- 滚动和触摸监听优先使用 passive listener。
- `localStorage` 数据保持最小化并设置版本，避免结构升级时读取旧格式。

## 5. 减少重复渲染

- 不要订阅只会在事件回调中读取的状态。
- 昂贵计算拆到可缓存组件或合理的 `useMemo` 中。
- 简单原始值计算不要滥用 `useMemo`。
- Effect 依赖尽量使用稳定的原始值。
- 能在 render 中推导的状态，不要用 Effect 再同步一份。
- `setState` 依赖旧值时使用函数式更新。
- 昂贵初始值使用 `useState(() => value)`。
- 非紧急更新使用 `startTransition`。
- 昂贵派生界面可使用 `useDeferredValue`。
- 高频但不影响渲染的数据放在 `useRef`。
- 禁止在组件函数内部定义新的组件类型。

## 6. 渲染性能

- 动画作用于 SVG 外层容器，而不是频繁改 SVG 内部属性。
- 长列表使用虚拟化或 `content-visibility`。
- 静态 JSX 提升到组件外部。
- 减少 SVG 坐标精度和无用节点。
- 客户端专属数据要设计无闪烁 hydration 方案。
- 只有确实可预期的差异才使用 hydration warning suppression。
- 条件渲染优先使用清晰的三元表达式，避免 `0 && <Node />` 之类错误输出。
- 使用资源提示预加载关键字体、图片和连接。
- 外部脚本根据依赖关系使用 `defer` 或 `async`。

## 7. JavaScript 性能

- 批量修改 DOM 样式，避免读写交替造成 layout thrashing。
- 重复查找先构建 `Map` 或 `Set`。
- 循环中缓存频繁访问的对象属性和函数结果。
- 合并连续的 `filter`、`map`、`reduce`，避免无意义中间数组。
- 先做廉价的长度或空值检查，再做昂贵比较。
- 及时返回，缩短执行路径。
- 正则表达式移出循环。
- 求最小值和最大值时避免为此排序整个数组。
- 需要保持不可变时使用 `toSorted()`，不要直接修改原数组。
- 非关键工作使用 `requestIdleCallback` 或调度机制延后。

## 审查流程

1. 找出所有异步边界，画出请求依赖关系。
2. 检查首屏 Bundle 中是否包含非必要模块。
3. 检查 Server/Client Component 边界和序列化数据。
4. 用 React Profiler 或运行数据定位重复渲染。
5. 只在测量后做微优化。
6. 每次修改都用测试、构建结果或性能数据验证。

## 输出要求

审查代码时，按以下格式报告：

```markdown
### 严重：请求瀑布
- 位置：
- 当前行为：
- 性能影响：
- 修改方案：
- 验证方法：
```

按“严重、高、中、低”排序；不要把格式偏好冒充性能问题。

## 边界

- 不为追求微小基准分数牺牲可读性和正确性。
- 不在没有测量证据时大规模重写。
- 不把所有组件都强行 `memo`。
- 不为了并行而破坏真实依赖、事务顺序或权限检查。
- 任何优化必须保持行为一致，并通过测试和实际运行验证。

## 来源

基于 Vercel Engineering 的 `vercel-react-best-practices` Skill 进行中文化整理，保留原始 Skill 名以确保自动触发和生态兼容。
