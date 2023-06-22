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
		Routing.RegisterRoute(nameof(ArtifactInformationView), typeof(ArtifactInformationView));
		Routing.RegisterRoute(nameof(UpdateStatusView), typeof(UpdateStatusView));
		Routing.RegisterRoute(nameof(ChangePasswordView), typeof(ChangePasswordView));

	}

    
}
