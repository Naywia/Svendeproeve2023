using Arkaeologigalleriet.Views;

namespace Arkaeologigalleriet;

public partial class AppShell : Shell
{
	public AppShell()
	{
		InitializeComponent();

		Routing.RegisterRoute(nameof(EmployeeView), typeof(EmployeeView));
		Routing.RegisterRoute(nameof(SearchView), typeof(SearchView));
		Routing.RegisterRoute(nameof(ScanQRView), typeof(ScanQRView));
	}
}
