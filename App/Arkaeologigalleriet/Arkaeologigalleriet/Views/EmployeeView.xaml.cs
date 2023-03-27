using Arkaeologigalleriet.ViewModels;

namespace Arkaeologigalleriet.Views;

public partial class EmployeeView : ContentPage
{
	public EmployeeView(EmployeeViewModel vm)
	{
		InitializeComponent();
		BindingContext= vm;
		Shell.SetFlyoutBehavior(this, FlyoutBehavior.Flyout);

		
	}
}