using Arkaeologigalleriet.ViewModels;
using CommunityToolkit.Maui.Views;

namespace Arkaeologigalleriet.Views;

public partial class LoginPopupView : ContentPage
{
    LoginViewModel _vm;

    public LoginPopupView()
	{
		InitializeComponent();
        _vm = new LoginViewModel();
	}

    protected override bool OnBackButtonPressed()
    {
        return true;
    }

    private async void EmpLoginBtn(object sender, EventArgs e) 
    {
        var loginresponce = await _vm.Login();
        if (loginresponce != null)
        {
            //await Application.Current.MainPage.Navigation.PopModalAsync();
        }
        else
        {
            await DisplayAlert("Fejl", "Fejl i bruger navn eller kode. Prøv igen", "Ok");
        }
    }
}