using Arkaeologigalleriet.Models;
using CommunityToolkit.Mvvm.Input;
using Newtonsoft.Json;
using System;

namespace Arkaeologigalleriet.ViewModels
{
    public partial class LoginViewModel
    {
        HttpClient _client;
        //string _url = "http://192.168.1.100:8000/";
        string _url = "http://164.68.113.72:8000/";
        

        public LoginViewModel()
        {

        }

        
        public async Task<LoginResponceModel> Login(string email = "aand@ag.dk", string password = "Andersine")
        {
            LoginResponceModel loginResponce = new();
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
                        await SecureStorage.Default.SetAsync("JWT", headers.GetValues("Authorization").First().Replace("Bearer ", ""));
                    }

                    string payload = await response.Content.ReadAsStringAsync();
                    try
                    {
                        loginResponce = JsonConvert.DeserializeObject<LoginResponceModel>(payload);
                    }
                    catch (Exception ex)
                    {
                        Console.Out.WriteLine(ex.Message);
                        return null;
                    }
                    
                    await App.ShellViewModel.GetUserDetalis(loginResponce.employeeID);
                    await Application.Current.MainPage.Navigation.PopModalAsync();
                    return loginResponce;
                }
            }
            catch (Exception ex)
            {
                Console.Out.WriteLine(ex.Message);
                return null;
            }
            return null;
        }
    }

    
}
