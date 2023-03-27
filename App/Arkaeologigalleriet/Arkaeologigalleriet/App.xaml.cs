using Arkaeologigalleriet.Views;

namespace Arkaeologigalleriet;

public partial class App : Application
{
	public App()
	{
		InitializeComponent();

		//MainPage = new AppShell();
		MainPage = new SearchView(null);
	}
}
