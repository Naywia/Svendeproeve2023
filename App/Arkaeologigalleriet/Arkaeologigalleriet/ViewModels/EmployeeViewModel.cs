using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

namespace Arkaeologigalleriet.ViewModels
{
    public partial class EmployeeViewModel : ObservableObject
    {
        [RelayCommand]
        async Task Logud()
        {
            await Shell.Current.GoToAsync("../");
        }
    }
}
