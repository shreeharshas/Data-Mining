using System;
using System.Collections.Generic;
using System.Data;
using Microsoft.VisualBasic.FileIO;
using System.Linq;
using System.Diagnostics;
using System.Runtime.InteropServices;

namespace DecisionTree
{
    public class SimpleNode
    {
        string name;
        string nodetype;
        List<SimpleNode> children;
        DataHolder associated_dataholder;

        public string Name
        {
            get
            {
                return name;
            }

            set
            {
                name = value;
            }
        }

        public string Nodetype
        {
            get
            {
                return nodetype;
            }

            set
            {
                nodetype = value;
            }
        }

        public List<SimpleNode> Children
        {
            get
            {
                return children;
            }

            set
            {
                children = value;
            }
        }

        public DataHolder Associated_dataholder
        {
            get
            {
                return associated_dataholder;
            }

            set
            {
                associated_dataholder = value;
            }
        }

        public SimpleNode()
        {
            Name = null;
            Nodetype = null;
            Children = null;
            Associated_dataholder = null;
        }

        public void initNode(string name, string nodetype, List<SimpleNode> children, DataHolder associated_dataholder)
        {
            Name = name;
            Nodetype = nodetype;
            Children = children;
            Associated_dataholder = associated_dataholder;
        }

        public SimpleNode getNode()
        {
            return this;
        }

        public void addChild(object childname, string childtype)
        {
            if (Children == null)
                Children = new List<SimpleNode>();

            if (childname is SimpleNode)
            {
                Children.Add((SimpleNode)childname);
            }
            else
            {
                SimpleNode ch = new SimpleNode();
                ch.initNode((string)childname, "default", null, null);
                Children.Add(ch);
            }
        }
    }

    public class DataHolder
    {
        DataTable dataset;
        List<string> featurestoexclude;
        //List<string> excluded_features;
        int len_dataset;
        bool isPure;  // getPureClass
        List<string> classes;  // calc_class_list
        List<string> features_list;  // calc_feature_list
        Dictionary<string, List<string>> feature_uniqueValues;  // calc_unique_feature_values
        double entropy;  // calc_entropy
        Dictionary<string, double> info_gain_features_map;  // calc_gain
        string best_feature;  // calc_best_feature
        Dictionary<string, int> class_counts;  // calc_class_counts
        int number_of_features;  // setNumberofFeatures

        public DataTable Dataset
        {
            get
            {
                return dataset;
            }

            set
            {
                dataset = value;
            }
        }

        public List<string> Featurestoexclude
        {
            get
            {
                return featurestoexclude;
            }

            set
            {
                featurestoexclude = value;
            }
        }

        public int Len_dataset
        {
            get
            {
                return len_dataset;
            }

            set
            {
                len_dataset = value;
            }
        }

        public bool IsPure
        {
            get
            {
                return isPure;
            }

            set
            {
                isPure = value;
            }
        }

        public List<string> Classes
        {
            get
            {
                return classes;
            }

            set
            {
                classes = value;
            }
        }

        public List<string> Features_list
        {
            get
            {
                return features_list;
            }

            set
            {
                features_list = value;
            }
        }

        public Dictionary<string, List<string>> Feature_uniqueValues
        {
            get
            {
                return feature_uniqueValues;
            }

            set
            {
                feature_uniqueValues = value;
            }
        }

        public double Entropy
        {
            get
            {
                return entropy;
            }

            set
            {
                entropy = value;
            }
        }

        public Dictionary<string, double> Info_gain_features_map
        {
            get
            {
                return info_gain_features_map;
            }

            set
            {
                info_gain_features_map = value;
            }
        }

        public Dictionary<string, int> Class_counts
        {
            get
            {
                return class_counts;
            }

            set
            {
                class_counts = value;
            }
        }

        public int Number_of_features
        {
            get
            {
                return number_of_features;
            }

            set
            {
                number_of_features = value;
            }
        }

        public string Best_feature
        {
            get
            {
                return best_feature;
            }

            set
            {
                best_feature = value;
            }
        }


        // Public Methods

        public DataHolder(DataTable inpdataset, List<string> excluded_features)
        {
            Dataset = inpdataset;
            if (excluded_features != null)
            {
                removeFeatures(excluded_features);
            }

            //Len_dataset = 0;
            //IsPure = false;  // getPureClass
            //Classes = null;  // calc_class_list
            //Features_list = null;  // calc_feature_list
            //Feature_uniqueValues = null;  // calc_unique_feature_values
            //Entropy = 0.0;  // calc_entropy
            //Info_gain_features_map = null;  // calc_gain
            //Best_feature = null;  // calc_best_feature
            //Class_counts = null;  // calc_class_counts
            //Number_of_features = 0;  // setNumberofFeatures
        }

        public void setLengthOfDS()
        {
            if (Dataset == null)
                Len_dataset = 0;
            else if (Dataset.Rows.Count == 0)
                Len_dataset = 0;
            else
                Len_dataset = Dataset.Rows.Count;
        }

        public void setNumberofFeatures()
        {
            if (Dataset == null)
                Number_of_features = 0;
            else if (Dataset.Rows.Count == 0)
                Number_of_features = 0;
            else
                //Number_of_features = Dataset.Rows[0].ItemArray.Length;
                Number_of_features = Dataset.Columns.Count;
        }

        public void calc_feature_list()
        {
            if (Len_dataset > 0)
            {
                if (Features_list == null)
                    Features_list = new List<string>();
            }
            if (Dataset.Rows.Count > 0)
            {
                for (int i = 0; i < Dataset.Rows[0].ItemArray.Length; i++)
                {
                    if (!Features_list.Contains(i.ToString()))
                        Features_list.Add(i.ToString());
                }
            }
        }

        public void calc_class_list()
        {
            if (Classes == null)
                Classes = new List<string>();
            foreach (DataRow datarow in Dataset.Rows)
                Classes.Add(Convert.ToString(datarow[Number_of_features - 1]));
        }

        public void calcclassCounts()
        {
            if (Len_dataset > 0)
            {
                int count = 0;
                if (Class_counts == null)
                    Class_counts = new Dictionary<string, int>();

                foreach (string uniq_class in Feature_uniqueValues[(Number_of_features - 1).ToString()])
                {
                    for (int i = 0; i < Dataset.Rows.Count; i++)
                        if (Convert.ToString(Dataset.Rows[i].ItemArray[Number_of_features - 1]) == uniq_class)
                            count++;
                    Class_counts[uniq_class] = count;
                }
            }
        }

        public void calc_unique_feature_values()
        {
            if (Len_dataset > 0)
            {
                foreach (string feat in Features_list)
                {
                    List<string> u_list = new List<string>();
                    bool goAhead = false;
                    if (Featurestoexclude == null)
                    {
                        goAhead = true;
                    }
                    else
                        if (!Featurestoexclude.Contains(feat))
                        goAhead = true;                      

                    if (goAhead)
                    {
                        foreach (DataRow datarow in Dataset.Rows)
                        {
                            string val = Convert.ToString(datarow.ItemArray[int.Parse(feat)]);
                            if (!u_list.Contains(val))
                                u_list.Add(val);
                        }
                    }
                
                    if (Feature_uniqueValues == null)
                        Feature_uniqueValues = new Dictionary<string, List<string>>();
                    Feature_uniqueValues[feat] = u_list;
                }
            }
        }


        public string getPureClass()
        {
            List<string> temp_class_list = new List<string>();
            foreach (DataRow datarow in Dataset.Rows)
            {
                string temp_class_name = Convert.ToString(datarow[Number_of_features - 1]);
                if (!temp_class_list.Contains(temp_class_name))
                    temp_class_list.Add(temp_class_name);
            }
            if (temp_class_list.Count == 1)
            {
                IsPure = true;
                return temp_class_list[0];
            }
            else
            {
                IsPure = false;
                return null;
            }
        }

        public string getMajorityClass()
        {
            if (Len_dataset > 0)
            {
                return Class_counts.Aggregate((l, r) => l.Value > r.Value ? l : r).Key;
            }
            return null;
        }

        public void setMajorityClass()
        {
            foreach (string clas in Classes)
            {
                int clas_counter = 0;
                foreach (DataRow datarow in Dataset.Rows)
                {
                    if (Convert.ToString(datarow[Number_of_features - 1]) == clas)
                        clas_counter++;
                }
                Class_counts[clas] = clas_counter;
            }
        }

        public bool IsEmpty()
        {
            if (Dataset == null)
                return true;
            else
            {
                if (Dataset.Rows.Count == 0)
                    return true;
            }
            return false;
        }

        //public List<string> split(string feature_name, double value) {
        //    List<string> retDataset = new List<string>();
        //    foreach (DataRow datarow in this.Dataset.Rows) {
        //        if (Convert.ToString(datarow.ItemArray[int.Parse(feature_name)]) == value)
        //            retDataset.Add(datarow);
        //    }
        //    return retDataset;
        //}

        public bool hasFeatures()
        {
            if (Features_list == null)
                return false;
            else if (Features_list.Count == 0)
                return false;
            return true;
        }

        public void calc_entropy()
        {
            setLengthOfDS();
            setNumberofFeatures();
            calc_feature_list();
            // this.removeFeatures();
            calc_unique_feature_values();
            calcclassCounts();
            calc_class_list();
            setMajorityClass();
            getPureClass();
            // E(S) = sigma(-p log(p)) where p is the ratio of number of examples of particular class to total number of examples
            if (Len_dataset > 0)
            {
                double e_of_s = 0.0;
                int denominator = Dataset.Rows.Count;
                foreach (string uniq_class in Feature_uniqueValues[Convert.ToString(Number_of_features - 1)])
                {  // last feature is the class
                    int numerator = Class_counts[uniq_class];
                    double p = (double)(numerator) / denominator;
                    if (p > 0)
                    {
                        double minus_p = -1 * p;
                        double lg_p = Math.Log(p, 2);
                        e_of_s += minus_p * lg_p;  // greater than one but less than log(len(unique_classes) to base 2)
                    }
                }
                // print "entropy of dataset:\n" + str(dataset) + "\nis:" + str(e_of_s)
                Entropy = e_of_s;
            }
        }

        public DataTable getSubset(string value_f, string feature)
        {
            return Dataset.Select("[" + feature + "] = '" + value_f + "'").CopyToDataTable();
        }

        public double set_gains(string inp_feature)
        {
            double sum_of_entropies_weighted_by_proportion = 0;
            int s_dataset = Dataset.Rows.Count;
            foreach (string unique_feature_value in Feature_uniqueValues[inp_feature])
            {
                DataTable temp_newds = getSubset(unique_feature_value, inp_feature);
                int s_newds = temp_newds.Rows.Count;
                double e_of_newds = 0.0;
                double proportion = 0;
                if (s_newds != 0)
                {
                    proportion = (double)(s_newds) / s_dataset;
                    e_of_newds = StarterClass.get_entropy(temp_newds, null);
                }
                sum_of_entropies_weighted_by_proportion += proportion * e_of_newds;
            }
            double infogain = Entropy - sum_of_entropies_weighted_by_proportion;
            return infogain;
        }

        public void calc_gain()
        {
            setLengthOfDS();
            setNumberofFeatures();
            calc_feature_list();
            calc_unique_feature_values();
            calcclassCounts();
            calc_class_list();
            setMajorityClass();
            getPureClass();
            calc_entropy();

            if (Len_dataset > 0)
            {
                if (Info_gain_features_map == null)
                    Info_gain_features_map = new Dictionary<string, double>();
                foreach (string feature_name in Features_list)
                {
                    if (Featurestoexclude == null)
                        Featurestoexclude = new List<string>();
                    if (!Featurestoexclude.Contains(feature_name) && feature_name != (Number_of_features - 1).ToString())
                        Info_gain_features_map[feature_name] = set_gains(feature_name);
                }
            }
        }//info gain <-- dont consider max if it is in the excluded features list

        public void calc_best_feature()
        {
            /*foreach (string s in Featurestoexclude)
                Info_gain_features_map.Remove(s);*/

            if (Len_dataset > 0)
                if(Info_gain_features_map.Count>0)
                    Best_feature = Info_gain_features_map.Aggregate((l, r) => l.Value > r.Value ? l : r).Key;
        }

        public void removeFeatures(List<string> features_to_remove)
        {
            if (Featurestoexclude == null)
            {
                Featurestoexclude = new List<string>();
            }
            if (features_to_remove != null)
            {
                foreach (string fe in features_to_remove)
                {
                    if (!Featurestoexclude.Contains(fe))
                        Featurestoexclude.Add(fe);
                }
            }
        }

        public void CalculateWhatIsNeededForEntropy()
        {
            calc_entropy();
        }

        public void CalculateNumbers()
        {
            calc_gain();
            calc_best_feature();
            //this.calc_gini();
        }
    }

    public class StarterClass
    {
        [DllImport("user32.dll")]
        public static extern bool ShowWindow(System.IntPtr hWnd, int cmdShow);

        public SimpleNode findSatisfyingChild(SimpleNode node, string value)
        {
            foreach (SimpleNode child in node.Children)
            {
                if (child.Name == value)
                {
                    return child;
                }
            }
            return null;
        }

        public void print_node(SimpleNode ch)
        {
            if (ch != null)
            {
                Console.WriteLine(ch.Nodetype + " " + ch.Name);
                if (ch.Children != null)
                {
                    foreach (SimpleNode child in ch.Children)
                    {
                        print_node(child);
                    }
                }
            }
        }

        public static int getCounts(DataTable dataset, string uniq_class, int num_feat)
        {
            int count = 0;
            foreach (DataRow datarow in dataset.Rows)
            {
                if (Convert.ToString(datarow[num_feat - 1]) == uniq_class)
                    count += 1;
            }
            return count;
        }

        public static List<string> get_unique_feature_values_dict(DataTable dataset, int input_feature)
        {
            List<string> uniqueList = new List<string>();
            foreach (DataRow datarow in dataset.Rows)
            {
                string s = Convert.ToString(datarow[input_feature]);
                if (!uniqueList.Contains(s))
                    uniqueList.Add(s);
            }
            return uniqueList;
        }

        public static double get_entropy(DataTable dataset, List<string> features_not_to_use)
        {
            double e_of_s = 0.0;
            int sizeofds = dataset.Rows.Count;
            if (sizeofds > 0)
            {
                int n_of_feat = dataset.Columns.Count - 1;
                int denominator = sizeofds;
                List<string> uniqLst = get_unique_feature_values_dict(dataset, n_of_feat - 1);
                foreach (string uniq_class in uniqLst)
                {   // last feature is the class){
                    double numerator = getCounts(dataset, uniq_class, n_of_feat);
                    double p = (double)(numerator) / denominator;
                    if (p > 0)
                    {
                        double minus_p = -1 * p;
                        double lg_p = Math.Log(p, 2);
                        e_of_s += minus_p * lg_p;  // greater than one but less than log(len(unique_classes) to base 2)
                    }
                }
            }
            return e_of_s;
        }

        public Dictionary<int, bool> getNonNumericFeatures(DataRow datarow)
        {   // returns a dictionary of features with indication of whether they are numeric or not
            Dictionary<int, bool> featureType = new Dictionary<int, bool>();
            for (int i = 0; i < datarow.ItemArray.Length; i++)
            {
                if (!(datarow[i] is int) || !(datarow[i] is float))
                    featureType[i] = false;
                else
                    featureType[i] = true;

            }
            return featureType;
        }

        public bool isContinuous(DataTable dataset, string feature)
        {
            List<string> single_feature_values_list = new List<string>();
            foreach (DataRow datarow in dataset.Rows)
            {
                string s = Convert.ToString(datarow[feature]);
                if (!single_feature_values_list.Contains(s))
                    single_feature_values_list.Add(s);
            }

            if (((double)(single_feature_values_list.Count) / dataset.Rows.Count) >= 0.7)
                return true;
            else
                return false;
        }

        public void discretize(DataTable dataset, List<string> features)
        {
            foreach (DataRow datarow in dataset.Rows)
            {
                List<int> list_feature_values = new List<int>();
                foreach (string feature in features)
                {
                    list_feature_values.Add(int.Parse((string)datarow.ItemArray[int.Parse(feature)]));

                    int min_of_f_column, max_of_f_column;
                    setMinMax(list_feature_values, out min_of_f_column, out max_of_f_column);


                    double numer = double.Parse((string)datarow[int.Parse(feature)]) - min_of_f_column;
                    double denom = max_of_f_column - min_of_f_column;

                    if (denom != 0)
                        datarow[int.Parse(feature)] = numer / denom;
                }
            }
        }

        private void setMinMax(List<int> list_feature_values, out int min_of_f_column, out int max_of_f_column)
        {
            min_of_f_column = 0;
            max_of_f_column = 0;
            foreach (int j in list_feature_values)
            {
                min_of_f_column = Math.Min(min_of_f_column, j);
                min_of_f_column = Math.Max(max_of_f_column, j);
            }
        }

        public object classify(DataRow datarow, SimpleNode node)
        {
            if (node != null)
            {
                if (node.Nodetype == "feature")
                {
                    List<SimpleNode> children = node.Children;
                    if (children != null)
                    {
                        SimpleNode s_child = findSatisfyingChild(node, (string)datarow[node.Name]);
                        if (s_child == null)
                        {
                            node.Associated_dataholder.CalculateWhatIsNeededForEntropy();
                            return node.Associated_dataholder.getMajorityClass();
                        }
                        else
                        {
                            SimpleNode feature_or_class_node = s_child.Children[0];
                            if (feature_or_class_node.Nodetype == "feature")
                                return classify(datarow, feature_or_class_node);
                            else
                                return feature_or_class_node;
                        }
                    }
                    else
                        return node;
                }
                else if (node.Nodetype == "value")
                {
                    SimpleNode feature_or_class_node = node.Children[0];
                    if (feature_or_class_node.Nodetype == "feature")
                        return classify(datarow, feature_or_class_node);
                    else
                        return node;
                }
                else
                    return node;
            }
            else
                return node;
        }

        public SimpleNode buildtree(object nd, DataHolder dataholder, List<string> features_to_exclude, string default_class)
        {
            dataholder.CalculateNumbers();
            SimpleNode root = null;
            if (dataholder.IsPure)
            {
                root = new SimpleNode();
                root.initNode(dataholder.getPureClass(), "class", null, dataholder);
                return root;
            }

            if (dataholder.Features_list != null)
            {
                /*if (dataholder.Featurestoexclude == null) {
                    default_class = dataholder.getMajorityClass();
                    root = new SimpleNode();
                    root.initNode(default_class, "class", null, dataholder);
                    //return root;
                }
                else */
                int lhs = dataholder.Featurestoexclude != null ? dataholder.Featurestoexclude.Count : 0;
                int rhs = dataholder.Features_list != null ? dataholder.Features_list.Count - 1 : 0;
                if (lhs == rhs)
                {
                    default_class = dataholder.getMajorityClass();
                    root = new SimpleNode();
                    root.initNode(default_class, "class", null, dataholder);
                    //return root;
                }
                else
                {
                    root = new SimpleNode();
                    root.initNode(dataholder.Best_feature, "feature", null, dataholder);
                    foreach (string uniq in dataholder.Feature_uniqueValues[dataholder.Best_feature])
                    {
                        DataHolder new_dholder = new DataHolder(dataholder.getSubset(uniq, dataholder.Best_feature), dataholder.Featurestoexclude);
                        new_dholder.CalculateNumbers();
                        SimpleNode node = new SimpleNode();
                        node.initNode(uniq, "value", null, new_dholder);

                        if (new_dholder.IsEmpty())
                        {
                            node.addChild(dataholder.getMajorityClass(), "class");
                        }
                        else
                        {
                            if (features_to_exclude == null)
                                features_to_exclude = new List<string>();
                            features_to_exclude.Add(new_dholder.Best_feature);
                            new_dholder.removeFeatures(features_to_exclude);
                            node.addChild(buildtree(uniq, new_dholder, features_to_exclude, default_class), null);
                        }
                        root.addChild(node, node.Nodetype);
                    }
                }
            }
            return root;
        }


        public DataTable readCSVFile(string FilePath)
        {
            DataTable dt = new DataTable();
            using (TextFieldParser parser = new TextFieldParser(FilePath))
            {
                parser.TextFieldType = FieldType.Delimited;
                parser.SetDelimiters("\t");
                while (!parser.EndOfData)
                {
                    string[] fields = parser.ReadFields();
                    if (fields.Length > 0)
                    {
                        if (dt.Columns.Count == 0)
                        {
                            for (int l = 0; l < fields.Length; l++)
                                dt.Columns.Add(l.ToString(), Type.GetType("System.String"));
                        }

                        DataRow dr = dt.NewRow();
                        for (int i = 0; i < fields.Length; i++)
                        {
                            dr[i] = fields[i];
                        }
                        dt.Rows.Add(dr);
                    }
                }
            }
            return dt;
        }
        public static void Main(string[] args)
        {
            Process p = Process.GetCurrentProcess();
            ShowWindow(p.MainWindowHandle, 3); //SW_MAXIMIZE = 3

            Console.WriteLine("reading train data...");
            StarterClass s = new StarterClass();
            
            DataTable dt = s.readCSVFile("zoo.data");

            List<string> autompg_data = new List<string>();
            Console.WriteLine("Reading and cleaning train data\n...");

            DataHolder dh = new DataHolder(dt, null);
            Console.WriteLine("finished reading and cleaning data\nBuilding tree...");
            SimpleNode node = s.buildtree(null, dh, null, null);

            Console.WriteLine("built tree\nreading test data...");
            // validation begins
            DataTable autompg_test = s.readCSVFile("zoo.test");
            //object classifiedNode = null;
            Console.WriteLine("finished reading and cleaning test\nstarting classification...");
            Dictionary<int, string> testingNodesList = new Dictionary<int, string>();
            Dictionary<int, string> classifiedNodesList = new Dictionary<int, string>();

            int i = 0;
            foreach (DataRow datarow in autompg_test.Rows)
            {
                testingNodesList[i] = (string)datarow[datarow.ItemArray.Length - 1];
                var classifiedNode = s.classify(datarow, node);
                classifiedNodesList[i] = classifiedNode is SimpleNode ? (((SimpleNode)classifiedNode).Name) : (string)classifiedNode;
                Console.WriteLine(string.Join(",", datarow.ItemArray) + " " + classifiedNodesList[i]);
                i++;
            }
            Console.Write("\nfinished classifying\ncalculating accuracy...");

            int predictedCorrectValues = 0;
            for (int m = 0; m < testingNodesList.Count; m++)
                if (testingNodesList[m] == classifiedNodesList[m])
                    predictedCorrectValues += 1;

            double accuracy = 0;
            if (testingNodesList.Count != 0)
                accuracy = (float)(predictedCorrectValues) / testingNodesList.Count * 100;
            Console.Write("Found Accuracy:" + accuracy + " %");
            Console.ReadKey();
        }
    }

}