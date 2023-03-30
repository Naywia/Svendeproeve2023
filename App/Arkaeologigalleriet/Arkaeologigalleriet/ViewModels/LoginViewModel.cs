using Android.OS;
using Newtonsoft.Json;

namespace Arkaeologigalleriet.ViewModels
{
    public partial class LoginViewModel
    {
        HttpClient _client;
        string _url = "http://192.168.1.100:8000/";

        public LoginViewModel()
        {
            
        }

        public async Task<LoginResponce> Login(string email = "ppedal@ag.dk", string password = "MandenMedDenGuleHat")
        {
            LoginResponce loginResponce = new LoginResponce();
            _client = new HttpClient();
            try
            {
                var nvc = new List<KeyValuePair<string, string>>
                {
                    new KeyValuePair<string, string>("username", email),
                    new KeyValuePair<string, string>("password", password)
                };

                HttpResponseMessage response = await _client.PostAsync(_url + "login", new FormUrlEncodedContent(nvc));
                if (response.IsSuccessStatusCode)
                {
                    var headers = response.Headers;
                    if (headers.Contains("Authorization"))
                    {
                        await SecureStorage.Default.SetAsync("JWT", headers.GetValues("Authorization").First());
                    }
                }
                string payload = await response.Content.ReadAsStringAsync();
                try
                {
                    loginResponce = JsonConvert.DeserializeObject<LoginResponce>(payload);
                }
                catch (Exception ex)
                {
                    Console.Out.WriteLine(ex.Message);
                    return null;
                }
            }
            catch (Exception ex)
            {
                Console.Out.WriteLine(ex.Message);
                return null;        
            }
            return loginResponce;
        }
    }

    public class LoginResponce
    {
        public string Responce { get; set; }
    }
}
