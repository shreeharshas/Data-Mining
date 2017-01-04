import java.util.ArrayList;
import java.util.HashMap;
//import java.util.Hashtable;
import java.util.List;
import java.util.Map.Entry;

public class DataHolder {
    String splitChar = "\t";
    ArrayList<String> Dataset;
    ArrayList<String> Featurestoexclude;
    //List<string> excluded_features;
    int Len_dataset;
    boolean IsPure;  // getPureClass
    ArrayList<String> Classes;  // calc_class_list
    ArrayList<String> Features_list;  // calc_feature_list
    HashMap<String, ArrayList<String>> Feature_uniqueValues;  // calc_unique_feature_values
    double Entropy;  // calc_entropy
    HashMap<String, Double> Info_gain_features_map;  // calc_gain
    String Best_feature;  // calc_best_feature
    HashMap<String, Integer> Class_counts;  // calc_class_counts
    int Number_of_features;  // setNumberofFeatures

    public DataHolder(ArrayList<String> inpdataset, ArrayList<String> excluded_features)
    {
        Dataset = new ArrayList<String>();
        for(String s : inpdataset){
            Dataset.add(s);
        }

        Featurestoexclude = new ArrayList<String>();
        removeFeatures(excluded_features);
        Info_gain_features_map = new HashMap<String, Double>();
        Features_list = new ArrayList<String>();
    }

    public void setLengthOfDS()
    {
        Len_dataset = (Dataset == null) ? 0 : Dataset.size();
    }

    public void setNumberofFeatures()
    {
        if (Dataset == null)
            Number_of_features = 0;
        else if (Dataset.size() == 0)
            Number_of_features = 0;
        else
            //Number_of_features = Dataset.Rows[0].ItemArray.Length;
            Number_of_features = Dataset.get(0).split(splitChar).length;
    }

    public void calc_feature_list()
    {
        if (this.Len_dataset > 0)
        {
            if(this.Features_list!=null) {
                this.Features_list = new ArrayList<String>();
            }

            for (int i = 0; i < this.Dataset.get(0).split(splitChar).length; i++) {
                if (!this.Features_list.contains(Integer.toString(i)))
                    this.Features_list.add(Integer.toString(i));
            }
        }
    }

    public void calc_class_list()
    {
        if (Classes == null)
            Classes = new ArrayList<String>();

        for(String datarow : Dataset)
            Classes.add(datarow.split(splitChar)[Number_of_features - 1]);
    }

    public void calcclassCounts()
    {
        if (this.Len_dataset > 0)
        {
            int count = 0;
            if (this.Class_counts == null)
                this.Class_counts = new HashMap<String, Integer>();

            /*for (HashMap.Entry<String, List<String>> entry : this.Feature_uniqueValues.entrySet()) {
                //System.out.println("Item : " + entry.getKey() + " Count : " + entry.getValue());
                if(entry.getKey()==)
            }*/
            ArrayList<String> ttt = this.Feature_uniqueValues.get(Integer.toString(Number_of_features - 1));
            for(String uniq_class : ttt)
            {
                for (String nextItem : this.Dataset)
                    if (nextItem.split(splitChar)[this.Number_of_features - 1].equals(uniq_class))
                        count++;
                this.Class_counts.remove(uniq_class);
                this.Class_counts.put(uniq_class, count);
            }
        }
    }

    public void calc_unique_feature_values()
    {
        if (Len_dataset > 0)
        {
            for (String feat : Features_list)
            {
                if (!Featurestoexclude.contains(feat))
                {
                    ArrayList<String> u_list = new ArrayList<String>();
                    for (String datarow : Dataset)
                    {
                        String val = datarow.split(splitChar)[Integer.parseInt(feat)];
                        if (!u_list.contains(val))
                            u_list.add(val);
                    }

                    if (Feature_uniqueValues == null)
                        Feature_uniqueValues = new HashMap<String, ArrayList<String>>();
                    Feature_uniqueValues.put(feat, u_list);
                }
            }
        }
    }

    public String getPureClass()
    {
        List<String> temp_class_list = new ArrayList<String>();
        for(String datarow : Dataset)
        {
            String temp_class_name = datarow.split(splitChar)[Number_of_features - 1];
            if (!temp_class_list.contains(temp_class_name))
                temp_class_list.add(temp_class_name);
        }
        if (temp_class_list.size() == 1)
        {
            IsPure = true;
            return temp_class_list.get(0);
        }
        else
        {
            IsPure = false;
            return null;
        }
    }

    public String getMajorityClass()
    {
        if (Len_dataset > 0)
        {
            Entry<String, Integer> max = null;
            for (Entry<String, Integer> e : Class_counts.entrySet()) {
                if (max == null || e.getValue() > max.getValue())
                    max = e;
            }
            return max.getKey();
        }
        return null;
    }

    public void setMajorityClass()
    {
        for (String clas : Classes)
        {
            int clas_counter = 0;
            for (String datarow : Dataset)
            {
                if (datarow.split(splitChar)[Number_of_features-1] == clas)
                    clas_counter++;
            }
            Class_counts.put(clas, clas_counter);
        }
    }

    public boolean IsEmpty()
    {
        if (Dataset == null)
            return true;
        else
        {
            if (Dataset.size() == 0)
                return true;
        }
        return false;
    }

    public boolean hasFeatures()
    {
        if (Features_list == null)
            return false;
        else if (Features_list.size() == 0)
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
        if (this.Len_dataset > 0)
        {
            Double e_of_s = 0.0;
            Integer denominator = this.Dataset.size();
            for (String uniq_class : this.Feature_uniqueValues.get(Integer.toString(this.Number_of_features - 1)))
            {  // last feature is the class
                int numerator = this.Class_counts.get(uniq_class);
                double p = (double)(numerator) / denominator;
                if (p > 0)
                {
                    double minus_p = -1 * p;
                    double lg_p = Math.log(p)/Math.log(2);
                    e_of_s += minus_p * lg_p;  // greater than one but less than log(len(unique_classes) to base 2)
                }
            }
            // print "entropy of dataset:\n" + str(dataset) + "\nis:" + str(e_of_s)
            this.Entropy = e_of_s;
        }
    }

    public ArrayList<String> getSubset(String value_f, String feature)
    {
        //System.out.println(feature+"="+value_f);
        ArrayList<String> retLst = new ArrayList<String>();
        for(String row : this.Dataset){
            String[] splitRow = row.split(splitChar);
            if(splitRow[Integer.parseInt(feature)].equals(value_f))
                retLst.add(row);
        }
        /*for(String s:retLst){
            System.out.println(s);
        }*/
        return retLst;
    }

    public double set_gains(String inp_feature)
    {
        double sum_of_entropies_weighted_by_proportion = 0;
        int s_dataset = Dataset.size();
        double e_of_newds = 0.0;
        double proportion = 0;

        for (String unique_feature_value : Feature_uniqueValues.get(inp_feature))
        {
            //System.out.println("inp_feature:"+inp_feature+", unique_feature_value:"+unique_feature_value);
            ArrayList<String> temp_newds = getSubset(unique_feature_value, inp_feature);
            int s_newds = temp_newds.size();

            if (s_newds == 0)
            {
                e_of_newds = 0;
                proportion = 0;
            }
            else
            {
                proportion = (double)(s_newds) / s_dataset;
                e_of_newds = StarterClass.get_entropy(temp_newds, null);
            }
            sum_of_entropies_weighted_by_proportion += proportion * e_of_newds;
        }
        double infogain = this.Entropy - sum_of_entropies_weighted_by_proportion;
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
                Info_gain_features_map = new HashMap<String, Double>();
            for (String feature_name : Features_list)
            {
                //System.out.println("feature_name:"+feature_name);
                if (Featurestoexclude == null)
                    Featurestoexclude = new ArrayList<String>();
                if (!Featurestoexclude.contains(feature_name) && !feature_name.equals(Integer.toString(Number_of_features - 1))) {
                    //System.out.println("calc_gain");
                    Info_gain_features_map.put(feature_name, set_gains(feature_name));
                }
            }
        }
    }//info gain <-- dont consider max if it is in the excluded features list

    public void calc_best_feature()
    {
        /*for (String s : Featurestoexclude)
            Info_gain_features_map.remove(s);*/

        if (Len_dataset > 0)
            if(Info_gain_features_map.size()>0){
                Entry<String, Double> max = null;
                for (Entry<String, Double> e : Info_gain_features_map.entrySet()) {
                    if (max == null || e.getValue() > max.getValue())
                        max = e;
                }
                Best_feature = max.getKey();
            }
    }

    public void removeFeatures(List<String> features_to_remove)
    {
        if (features_to_remove != null)
        {
            for (String fe : features_to_remove)
            {
                if (!Featurestoexclude.contains(fe))
                    Featurestoexclude.add(fe);
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
