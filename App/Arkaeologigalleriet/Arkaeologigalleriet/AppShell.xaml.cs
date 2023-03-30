using Arkaeologigalleriet.ViewModels;
using Arkaeologigalleriet.Views;

namespace Arkaeologigalleriet;

public partial class AppShell : Shell
{
	public AppShell()
	{
		InitializeComponent();

		BindingContext = App.ShellViewModel;
		Routing.RegisterRoute(nameof(EmployeeView), typeof(EmployeeView));
		Routing.RegisterRoute(nameof(SearchView), typeof(SearchView));
		Routing.RegisterRoute(nameof(ScanQRView), typeof(ScanQRView));
	}

    private async void LogOutBtn(object sender, EventArgs e)
    {
        await Application.Current.MainPage.Navigation.PushModalAsync(new LoginPopupView());
    }
}
