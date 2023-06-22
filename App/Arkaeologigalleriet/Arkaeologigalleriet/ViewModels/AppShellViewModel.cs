using Arkaeologigalleriet.Models;
using Arkaeologigalleriet.Views;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Newtonsoft.Json;
using System.ComponentModel;
using System.Net.Http.Headers;
using System.Runtime.CompilerServices;

namespace Arkaeologigalleriet.ViewModels
{
    public partial class AppShellViewModel : BaseViewModel
    {
        int _empId;
        HttpClient _client;


        string _url = "http://192.168.1.100:8000/";
        //string _url = "http://164.68.113.72:8000/";



        public AppShellViewModel()
        {

        }

        public async Task<EmployeeModel> GetUserDetalis(int empId)
        {
            _empId = empId;
            _client = new HttpClient();
            _employeeModel = new EmployeeModel();

            try
            {
                using HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Get, _url + "user?userID=" + _empId);
                request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", await SecureStorage.Default.GetAsync("JWT"));
                HttpResponseMessage response = await _client.SendAsync(request);
                if (response.IsSuccessStatusCode)
                {
                    string payload = await response.Content.ReadAsStringAsync();
                    try
                    {

                        var jsonObject = JsonConvert.DeserializeObject<RootUserModel>(payload);
                        foreach (var item in jsonObject.User)
                        {
                            //_employeeModel.FirstName = item.FirstName;
                            //_employeeModel.LastName = item.LastName;
                            //_employeeModel.Address = item.Address;
                            //_employeeModel.City = item.City;
                            //_employeeModel.Email = item.Email;
                            //_employeeModel.EmployeeType = item.EmployeeType;
                            //_employeeModel.ID = item.ID;
                            EmployeeModel = item;
                        }

                    }
                    catch (Exception ex)
                    {
                        Console.Out.WriteLine(ex.Message);
                        throw;
                    }
                    return _employeeModel;
                }
            }
            catch (Exception ex)
            {
                Console.Out.WriteLine(ex.Message);
                throw;
            }
            return null;
        }

        [RelayCommand]
        private async void ProfilNavi()
        {
            await Shell.Current.GoToAsync(nameof(EmployeeView), 
                new Dictionary<string, object>
                {
                    ["EmployeeModel"] = EmployeeModel
                }
            );
        }

        [RelayCommand]
        public async void LogoutBTN()
        {
            SecureStorage.Default.Remove("JWT");
            await Application.Current.MainPage.Navigation.PushModalAsync(new LoginPopupView());
        }


        private EmployeeModel _employeeModel;

        public EmployeeModel EmployeeModel
        {
            get { return _employeeModel; }
            set
            {
                _employeeModel = value;
                OnPropertyChanged(nameof(EmployeeModel));
            }
        }
    }
}
