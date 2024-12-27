defmodule BackendPerf.Client do
  @public_key """
  -----BEGIN PUBLIC KEY-----
  MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmIzophqDebSpnL77RK0l
  6l8TECsiW7t1+7ilLuc0OtPBFgRaIyEUhjV90XY1LJcWZ3UmdZ77GBoHRcZa0UAE
  8DF7seDu2yyXy2xE0i4gFo41WhOwIkV0SVlT7hQ+llf2w8Nk48efjjpz9v5Nf62I
  VxRBcDQq3BUbvq/ZHbkUs7jiAIp2DeW4FBL3gj7C4yaCkis0HOHFSqCGxDfDr8Vg
  Y9quJIoKfLDqMeXylBICW9tAdUSBC6nf8fdiFflvdenVb1VhZ64oseJMp+8Bqt5R
  wTHjucdOXlXbhM+pooTEKu+FyVQcwbwkjL0MM8SnZcfozP9ZAlSiO+5vewrqiOhB
  NwIDAQAB
  -----END PUBLIC KEY-----
  """
  def client(id, host) do
    public_key =
      @public_key |> :public_key.pem_decode() |> Enum.at(0) |> :public_key.pem_entry_decode()

    tmp = :crypto.strong_rand_bytes(8) |> Base.encode16()
    username = "#{tmp}_#{id}"
    email = "#{tmp}-#{id}@#{tmp}.com"
    password = :crypto.strong_rand_bytes(10) |> Base.encode64()
    password_encrypted = :public_key.encrypt_public(password, public_key) |> Base.encode64()

    if HTTPoison.request!(
         :post,
         "#{host}/users/register/",
         Jason.encode!(%{username: username, email: email, password_encrypted: password_encrypted}),
         [{"Content-Type", "application/json"}]
       ).status_code == 500,
       do: raise("500")

    access =
      HTTPoison.request!(
        :post,
        "#{host}/users/login/",
        Jason.encode!(%{email: email, password_encrypted: password_encrypted}),
        [{"Content-Type", "application/json"}]
      ).body
      |> Jason.decode!()
      |> Map.get("access")

    if HTTPoison.request!(:get, "#{host}/users/profile/", "", [
         {"Authorization", "Bearer #{access}"}
       ]).status_code ==
         500,
       do: raise("500")

    if HTTPoison.request!(
         :post,
         "#{host}/experiments/create/",
         Jason.encode!(%{
           title: username,
           description: username,
           person_wanted: 10,
           money_per_person: 10,
           activity_time: "2024-01-01",
           activity_location: "tmp"
         }),
         [{"Authorization", "Bearer #{access}"}, {"Content-Type", "application/json"}]
       ).status_code ==
         500,
       do: raise("500")
  end
end
