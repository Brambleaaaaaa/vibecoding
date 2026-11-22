# Vibe Coding · 产品仓库

把用 AI 辅助做出来的东西攒在一起。每个产品一个独立仓库，以 Git Submodule 挂在 `products/` 下，按编号排序。

- 在线产品：[词刻 CIKE](https://brambleaaaaaa.github.io/cike-multibook/)
- 作者主页：[Brambleaaaaaa](https://github.com/Brambleaaaaaa)
- 作品集：[portfolio](https://github.com/Brambleaaaaaa/portfolio)

## 产品列表

<!-- PRODUCTS:START -->
<!-- PRODUCTS:END -->

## 新增产品

复制仓库后，在根目录运行：

```powershell
python scripts/add_product.py `
  --name "产品名" `
  --slug "product-slug" `
  --repo "https://github.com/Brambleaaaaaa/product-slug" `
  --desc "一句话介绍" `
  --tags "React,TypeScript" `
  --demo "https://example.com"
```

脚本会：

1. 把新仓库作为 submodule 加到 `products/<编号>-<slug>`；
2. 更新 `products.json`；
3. 重新生成上面的产品列表；
4. 自动 `git add / commit / push`。

只改列表不新增仓库时，运行：

```powershell
python scripts/render_readme.py
```

## 约定

- 编号从 1 开始，按加入顺序递增，不重复使用。
- 每个产品保持独立仓库，本仓库只做索引，不复制源码。
- `products.json` 是唯一数据源，README 自动生成，不要手改列表区块。
