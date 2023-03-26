using Arkaeologigalleriet.ViewModels;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

namespace Arkaeologigalleriet.Views;

public partial class EmployeeView : ContentPage
{
	public EmployeeView(EmployeeViewModel vm)
	{
		InitializeComponent();
		BindingContext= vm;
		Shell.SetFlyoutBehavior(this, FlyoutBehavior.Flyout);
		Shell.Current.FlyoutIsPresented = true;

		
	}
}