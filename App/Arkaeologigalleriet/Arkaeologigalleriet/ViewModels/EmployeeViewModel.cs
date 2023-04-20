
using Arkaeologigalleriet.Models;
using Arkaeologigalleriet.Services;
using Arkaeologigalleriet.Views;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace Arkaeologigalleriet.ViewModels
{
    [QueryProperty(nameof(EmployeeModel), nameof(EmployeeModel))]
    public partial class EmployeeViewModel : BaseViewModel
    {

        ApiServices _apiServices;
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

        public EmployeeViewModel()
        {
            AppShell.Current.FlyoutIsPresented = false;
            _apiServices = new ApiServices();
        }

        [RelayCommand]
        public async void Updateinfo()
        {
            if (await _apiServices.UpdateEmpInfo(EmployeeModel) == true)
            {
                await Application.Current.MainPage.DisplayAlert("Succes", "Dine infomationer er belevet opdateret", "Ok");
            }
            else
            {
                await Application.Current.MainPage.DisplayAlert("Fejl", "Der skete en fejl. Prøv igen", "Ok");
            }
        }

        [RelayCommand]
        public async void NaviToChangePassword()
        {
            await Shell.Current.GoToAsync($"{nameof(ChangePasswordView)}?UserID={EmployeeModel.ID}");
        }

        
    }
}
