using Arkaeologigalleriet.ViewModels;
using Arkaeologigalleriet.Views;

namespace Arkaeologigalleriet;

public partial class MainPage : ContentPage
{

	public MainPage(MainPageViewModel vm)
	{
		InitializeComponent();
        BindingContext = vm;
        Shell.SetFlyoutBehavior(this, FlyoutBehavior.Disabled);
	}

    private async void LoginClicked(object sender, EventArgs e)
    {    
        await Shell.Current.GoToAsync(nameof(EmployeeView));
    }

    private void GuestLoginClicked(object sender, EventArgs e)
    {

    }

    
    
}

