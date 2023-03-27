using Arkaeologigalleriet.ViewModels;

namespace Arkaeologigalleriet.Views;

public partial class ArtifactInformationView : ContentPage
{
	public ArtifactInformationView(ArtifactInformationViewModel vm)
	{
		InitializeComponent();
		BindingContext = vm;
		Test.Text = "Title: Starry Night Over the Rhone\nKunstner: Vincent van Gogh\nDato: 1888\nMedium: Olie p� l�rred\nSt�rrelse: 72,5 x 92 cm\n\nVincent van Gogh, en af ??de mest ber�mte malere i historien, malede'Starry Night Over the Rhone' i 1888. Dette maleri viser en natlig scene langs Rh�ne-floden i Arles, Frankrig, hvor van Gogh boede p� det tidspunkt. Billedet viser en stjerneklar nattehimmel, der reflekterer i vandet p� Rh�ne-floden. To figurer kan ses p� kanten af ??floden, mens en b�d sejler forbi i baggrunden. Van Gogh brugte levende farver og b�rstestr�g for at skabe en intens og dr�mmende stemning i maleriet. 'Starry Night Over the Rhone' er en af ??van Goghs mest ikoniske v�rker og er nu en del af samlingen p� Mus�e d'Orsay i Paris.";
    }
}