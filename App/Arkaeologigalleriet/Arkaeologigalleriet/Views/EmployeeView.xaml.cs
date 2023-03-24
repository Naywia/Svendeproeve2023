namespace Arkaeologigalleriet.Views;

public partial class EmployeeView : ContentPage
{
	public EmployeeView()
	{
		InitializeComponent();
		Shell.SetFlyoutBehavior(this, FlyoutBehavior.Locked);
	}
}