defmodule BackendPerfTest do
  use ExUnit.Case
  import BackendPerf.Client

  defp concurrency(n) do
    IO.puts("n clients = #{n}")
    host = Application.get_env(:backend_perf, :host)
    tasks =
      for id <- 1..n do
        Task.async(fn -> client(id, host) end)
      end

    Enum.map(tasks, fn task ->
      Task.await(task)
    end)
  end

  test "concurrency" do
    concurrency(1)
    concurrency(2)
    concurrency(4)
    concurrency(8)
  end
end
