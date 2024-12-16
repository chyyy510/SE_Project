# BackendPerfTest, 后端性能测试

## 配置开发环境

1. 安装 [Erlang/OTP](https://www.erlang.org/) 27；
2. 安装 [Elixir](https://elixir-lang.org/) 1.17；
   对于 Windows，安装以上两者是简单的。对于 Linux（仅在 Ubuntu 24.04 测试），请依 [Install Elixir](https://elixir-lang.org/install.html#install-scripts) 操作。
3. （可选）为 Hex 包管理器配置中国大陆镜像源（又拍云）
   ```bash
   mix hex.config mirror_url https://hexpm.upyun.com
   ```
4. 克隆本仓库；
5. 运行 `mix deps.get` 获取依赖库；
6. 在启动后端的情况下，运行 `mix test` 测试。