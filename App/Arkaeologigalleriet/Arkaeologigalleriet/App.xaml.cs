using Arkaeologigalleriet.Views;

namespace Arkaeologigalleriet;

public partial class App : Application
{
	public App()
	{
		InitializeComponent();

		MainPage = new AppShell();
	}

    protected override void OnStart()
    {
        Current.MainPage.Navigation.PushModalAsync(new LoginPopupView());
    }
}
