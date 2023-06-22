using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Arkaeologigalleriet.Models
{

    public class StoragesModel
    {
        public List<StorageModel> Storage { get; set; }
    }

    public class StoragesListModel
    {
        public List<StorageModel> Storages { get; set; }
    }

    public class StorageModel
    {
        public int ID { get; set; }
        public string Name { get; set; }
    }
}
