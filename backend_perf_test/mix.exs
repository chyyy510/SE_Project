defmodule BackendPerfTest.MixProject do
  use Mix.Project

  def project do
    [
      app: :backend_perf_test,
      version: "0.1.0",
      elixir: "~> 1.17",
      start_permanent: Mix.env() == :prod,
      deps: deps()
    ]
  end

  def application do
    [
      extra_applications: [:logger]
    ]
  end

  defp deps do
    [
      {:httpoison, "~> 2.0"},
      {:jason, "~> 1.0"}
    ]
  end
end
