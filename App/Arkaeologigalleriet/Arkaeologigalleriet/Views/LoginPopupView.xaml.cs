using CommunityToolkit.Maui.Views;

namespace Arkaeologigalleriet.Views;

public partial class LoginPopupView : ContentPage
{
	public LoginPopupView()
	{
		InitializeComponent();
	}

    protected override bool OnBackButtonPressed()
    {
        return true;
    }

    private async void EmpLoginBtn(object sender, EventArgs e) 
    {
        await Application.Current.MainPage.Navigation.PopModalAsync();
    }
}