using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Arkaeologigalleriet.Models
{
    public class PlacementModels
    {
        public List<PlacementModel> Placements { get; set; }
    }

    public class SingelPlacementModel
    {
        public List<PlacementModel> Placement { get; set; }
    }

    public class PlacementModel
    {
        public int ID { get; set; }
        public string Storage { get; set; }
        public int Shelf { get; set; }
        public string Row { get; set; }
        public string DisplayText
        {
            get
            {
                return $"Shelf: {Shelf}, Row: {Row}";
            }
        }
    }
}
