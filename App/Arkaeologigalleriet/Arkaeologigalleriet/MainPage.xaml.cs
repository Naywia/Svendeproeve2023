using Arkaeologigalleriet.Views;

namespace Arkaeologigalleriet;

public partial class MainPage : ContentPage
{

	public MainPage()
	{
		InitializeComponent();
        Shell.SetFlyoutBehavior(this, FlyoutBehavior.Locked);
	}

    private async void LoginClicked(object sender, EventArgs e)
    {
        var Empview = new NavigationPage(new EmployeeView());
        await Navigation.PushAsync(Empview, true);
    }

    private void GuestLoginClicked(object sender, EventArgs e)
    {

    }

    
}

