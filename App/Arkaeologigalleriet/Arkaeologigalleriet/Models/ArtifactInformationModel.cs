using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;

namespace Arkaeologigalleriet.Models
{
    public class ArtifactInformationModel 
    {
        public List<Artefact> Artefact { get; set; }
    }

    public class ArtifactInformationModels
    {
        public List<Artefact> Artefacts { get; set; }
    }

    public class Artefact
    {
        public int ID { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        public string ArtefactType { get; set; }
        public string Storage { get; set; }
        public int Shelf { get; set; }
        public string Row { get; set; }
    }
}
