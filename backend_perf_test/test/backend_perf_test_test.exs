defmodule BackendPerfTestTest do
  use ExUnit.Case
  doctest BackendPerfTest

  defp concurrency_1(n) do
    IO.puts("n clients = #{n}")

    tasks =
      for id <- 1..n do
        Task.async(fn ->
          BackendPerfTest.Client.client(
            id,
            Application.get_env(:backend_perf_test, :host, "127.0.0.1:8000")
          )
        end)
      end

    Enum.map(tasks, fn task ->
      Task.await(task)
    end)
  end

  defp concurrency_2(n) do
    IO.puts("n clients = #{n}")

    tasks =
      for id <- 1..n do
        Task.async(fn ->
          BackendPerfTest.Client.client_2(
            id,
            Application.get_env(:backend_perf_test, :host, "127.0.0.1:8000")
          )
        end)
      end

    Enum.map(tasks, fn task ->
      Task.await(task)
    end)
  end

  @tag :first
  test "concurrency_1" do
    concurrency_1(1)
    concurrency_1(2)
    concurrency_1(4)
    concurrency_1(8)
  end

  @tag :second
  test "concurrency_2" do
    concurrency_2(1)
    concurrency_2(8)
    concurrency_2(64)
    concurrency_2(256)
    concurrency_2(512)
    concurrency_2(1024)
  end
end
