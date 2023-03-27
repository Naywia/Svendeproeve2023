using Arkaeologigalleriet.ViewModels;

namespace Arkaeologigalleriet.Views;

public partial class ArtifactInformationView : ContentPage
{
	public ArtifactInformationView(ArtifactInformationViewModel vm)
	{
		InitializeComponent();
		BindingContext = vm;
		Test.Text = "Title: Starry Night Over the Rhone\nKunstner: Vincent van Gogh\nDato: 1888\nMedium: Olie på lærred\nStørrelse: 72,5 x 92 cm\n\nVincent van Gogh, en af ??de mest berømte malere i historien, malede'Starry Night Over the Rhone' i 1888. Dette maleri viser en natlig scene langs Rhône-floden i Arles, Frankrig, hvor van Gogh boede på det tidspunkt. Billedet viser en stjerneklar nattehimmel, der reflekterer i vandet på Rhône-floden. To figurer kan ses på kanten af ??floden, mens en båd sejler forbi i baggrunden. Van Gogh brugte levende farver og børstestrøg for at skabe en intens og drømmende stemning i maleriet. 'Starry Night Over the Rhone' er en af ??van Goghs mest ikoniske værker og er nu en del af samlingen på Musée d'Orsay i Paris.";
    }
}