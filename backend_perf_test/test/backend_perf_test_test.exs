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

  test "concurrency_1_1",
    do: concurrency_1(1)

  test "concurrency_1_2",
    do: concurrency_1(1)

  test "concurrency_1_4",
    do: concurrency_1(4)

  test "concurrency_1_8",
    do: concurrency_1(8)

  # test "concurrency_2_1",
  #   do: concurrency_2(1)

  # test "concurrency_2_8",
  #   do: concurrency_2(8)

  # test "concurrency_2_64",
  #   do: concurrency_2(64)

  # test "concurrency_2_256",
  #   do: concurrency_2(256)

  # test "concurrency_2_512",
  #   do: concurrency_2(512)

  # test "concurrency_2_1024",
  #   do: concurrency_2(1024)
end
