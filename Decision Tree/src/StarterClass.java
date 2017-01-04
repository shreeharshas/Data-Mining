import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.*;
import java.io.PrintWriter;

public class StarterClass{
    public static int maincounter = 0;
    public SimpleNode findSatisfyingChild(SimpleNode node, String value)
    {
        for (SimpleNode child:node.Children)
        {
            if (child.Name.equals(value))
            {
                return child;
            }
        }
        return null;
    }
    static String splitChar = "\t";
    public void print_node(SimpleNode ch)
    {
        if (ch != null)
        {
            System.out.println(ch.Nodetype + " " + ch.Name);
            if (ch.Children != null)
            {
                for (SimpleNode child:ch.Children)
                {
                    print_node(child);
                }
            }
        }
    }

    public static int getCounts(ArrayList<String> dataset, String uniq_class, int num_feat)
    {
        int count = 0;
        for (String datarow:dataset)
        {
            String t = datarow.split(splitChar)[num_feat - 1];
            if (t.equals(uniq_class))
                count += 1;
        }
        return count;
    }

    public static ArrayList<String> get_unique_feature_values_dict(ArrayList<String> dataset, int input_feature)
    {
        ArrayList<String> uniqueList = new ArrayList<String>();
        for (String datarow:dataset)
        {
			//System.out.println(datarow.split(splitChar).length+":"+input_feature);
            String s = datarow.split(splitChar)[input_feature];
            if (!uniqueList.contains(s))
                uniqueList.add(s);
        }
        return uniqueList;
    }

    public static double get_entropy(ArrayList<String> dataset, ArrayList<String> features_not_to_use)
    {
        double e_of_s = 0.0;
        int sizeofds = dataset.size();
        if (sizeofds > 0)
        {
            int n_of_feat = dataset.iterator().next().split(splitChar).length;
            int denominator = sizeofds;
            ArrayList<String> uniqLst = get_unique_feature_values_dict(dataset, n_of_feat - 1);
            for (String uniq_class:uniqLst)
            {   // last feature instanceof the class){
                double numerator = getCounts(dataset, uniq_class, n_of_feat);
                double p = (double)(numerator) / denominator;
                if (p > 0)
                {
                    double minus_p = -1 * p;
                    double lg_p = Math.log(p)/ Math.log(2);
                    e_of_s += minus_p * lg_p;  // greater than one but less than log(len(unique_classes) to base 2)
                }
            }
        }
        return e_of_s;
    }


    public Object classify(String datarow, SimpleNode node)
    {
        if(node !=null)
        {
            if (node.Nodetype.equals("feature"))
            {
                ArrayList<SimpleNode> children = new ArrayList<SimpleNode>();
                if (node.Children != null)
                {
                    SimpleNode s_child = findSatisfyingChild(node, datarow.split(splitChar)[Integer.parseInt(node.Name)]);
                    if (s_child == null)
                    {
                        node.Associated_dataholder.CalculateWhatIsNeededForEntropy();
                        return node.Associated_dataholder.getMajorityClass();
                    }
                    else
                    {
                        SimpleNode feature_or_class_node = s_child.Children.get(0);
                        if (feature_or_class_node.Nodetype.equals("feature"))
                            return classify(datarow, feature_or_class_node);
                        else
                            return feature_or_class_node;
                    }
                }
            }
            else if (node.Nodetype.equals("value"))
            {
                SimpleNode feature_or_class_node = node.Children.get(0);
                if (feature_or_class_node.Nodetype.equals("feature"))
                    return classify(datarow, feature_or_class_node);
                else
                    return node;
            }
            else
                return node;
        }
        return null;
    }

    public SimpleNode buildtree(Object nd, DataHolder dataholder, ArrayList<String> features_to_exclude, String default_class)
    {
        dataholder.CalculateNumbers();
        maincounter++;
        //System.out.println("\n"+maincounter+"dataholder.CalculateNumbers();");
        SimpleNode root = null;
        if (dataholder.IsPure)
        {
            //System.out.println("dataholder.IsPure");
            root = new SimpleNode();
            root.initNode(dataholder.getPureClass(), "class", null, dataholder);
            return root;
        }

        if (dataholder.Features_list != null)
        {
            //System.out.println("dataholder.Features_list != null");
            int lhs = dataholder.Featurestoexclude != null ? dataholder.Featurestoexclude.size() : 0;
            int rhs = dataholder.Features_list.size() - 1;
            if (lhs == rhs)
            {
                //System.out.println("lhs==rhs");
                default_class = dataholder.getMajorityClass();
                root = new SimpleNode();
                root.initNode(default_class, "class", null, dataholder);
                return root;
            }
            else
            {
                //System.out.println("lhs!=rhs");
                root = new SimpleNode();
                root.initNode(dataholder.Best_feature, "feature", null, dataholder);
                for (String uniq : dataholder.Feature_uniqueValues.get(dataholder.Best_feature))
                {
                    DataHolder new_dholder = new DataHolder(dataholder.getSubset(uniq, dataholder.Best_feature),dataholder.Featurestoexclude);
                    new_dholder.CalculateNumbers();
                    SimpleNode node = new SimpleNode();
                    node.initNode(uniq, "value", null, new_dholder);

                    if (new_dholder.IsEmpty())
                    {
                        //System.out.println("new_dholder.IsEmpty()");
                        node.addChild(dataholder.getMajorityClass(), "class");
                    }
                    else
                    {
                        //System.out.println("new_dholder Is not Empty()");
                        if (features_to_exclude == null)
                            features_to_exclude = new ArrayList<String>();
                        features_to_exclude.add(new_dholder.Best_feature);
                        new_dholder.removeFeatures(features_to_exclude);
                        node.addChild(buildtree(uniq, new_dholder, features_to_exclude, default_class), null);
                    }
                    root.addChild(node, null);
                }
            }
        }
        return root;
    }


    public ArrayList<String> readCSVFile(String FilePath)
    {
        ArrayList<String> dt = new ArrayList<String>();
        try {
            BufferedReader br = new BufferedReader(new FileReader(FilePath));
            String line;
            while ((line = br.readLine()) != null) {
                dt.add(line);
            }
            br.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return dt;
    }

	
	public ArrayList<String> normalize(ArrayList<String> dataset){
		ArrayList<String> retList = new ArrayList<String>();
		for (String datarow : dataset){
			int feature =0;
			ArrayList<Double> list_feature_values = new ArrayList<Double>();
			for (; feature< datarow.split(splitChar).length;feature++){
				String d = datarow.split(splitChar)[feature];
				//System.out.println(d);
				list_feature_values.add(Double.parseDouble(d));
			}
			double min_of_f_column = Collections.min(list_feature_values,null);
			double max_of_f_column = Collections.max(list_feature_values,null);
//System.out.println(datarow);
String ss = datarow.split(splitChar)[feature-1];
			double numer = Double.parseDouble(ss) - min_of_f_column;
			double denom = max_of_f_column - min_of_f_column;
			double q = numer/denom;
			String s = "";
			if (denom != 0){
				String[] splitStr = datarow.split(splitChar);
				splitStr[feature-1] = Double.toString(q);
				s = String.join(",", splitStr);
			}
			retList.add(s);
		}
		return retList;
	}
	
	public ArrayList<Double> getMultiples(ArrayList<Double> inp, int spl){
		ArrayList<Double> a = new ArrayList<Double>();
		for(int i=0;i<inp.size();i+=spl){
			a.add(inp.get(i));
		}
		return a;
	}
		
	public ArrayList<String> discretize(ArrayList<String> dataset){
		HashMap<Integer, ArrayList<Double>> list_feature_valus = new HashMap<Integer, ArrayList<Double>>();
		for(String datarow : dataset){
			String[] drowsplit = datarow.split(",");
			for (int feature=0; feature < drowsplit.length; feature++){
				//System.out.println(drowsplit[feature]);
				double df = Double.parseDouble(drowsplit[feature]);

				if (!list_feature_valus.containsKey(feature)){
					ArrayList<Double> tempRow = new ArrayList<Double>();
					tempRow.add(df);
					list_feature_valus.put(feature, tempRow);
				}
				else{
					ArrayList<Double> tempRow = list_feature_valus.get(feature);
					tempRow.add(df);
					list_feature_valus.put(feature, tempRow);
				}
			}
		}
		
		ArrayList<String> retList = new ArrayList<String>();
		for(String datarow : dataset){
			String[] drSplit = datarow.split(",");
			for (int feature=0; feature < drSplit.length; feature++){
				ArrayList<Double> sorted_list = list_feature_valus.get(feature);
				Collections.sort(sorted_list);
				int spl = (int)(sorted_list).size()/10;
				ArrayList<Double> lst = getMultiples(sorted_list, spl);

				double d_val = Double.parseDouble(drSplit[feature]);
				if (d_val >= lst.get(9))
					drSplit[feature] = "10";
				else if (d_val >= lst.get(8))
					drSplit[feature] = "9";
				else if (d_val >= lst.get(7))
					drSplit[feature] = "8";
				else if (d_val >= lst.get(6))
					drSplit[feature] = "7";
				else if (d_val >= lst.get(5))
					drSplit[feature] = "6";
				else if (d_val >= lst.get(4))
					drSplit[feature] = "5";
				else if (d_val >= lst.get(3))
					drSplit[feature] = "4";
				else if (d_val >= lst.get(2))
					drSplit[feature] = "3";
				else if (d_val >= lst.get(1))
					drSplit[feature] = "2";
				else if (d_val >= lst.get(0))
					drSplit[feature] = "1";
				else
					drSplit[feature] = "0";
				}
				retList.add(String.join(",",drSplit));
			}
			return retList;
	}
	
    public static void main(String[] args)
    {
        System.out.println("reading train data...");
        StarterClass s = new StarterClass();

        ArrayList<String> dt = s.readCSVFile("..\\data\\eval\\2005_2006.txt");

        System.out.println("Reading and cleaning train data, Normalizing\n...");

		//ArrayList<String> normalized = s.normalize(dt);
		//ArrayList<String> dtrain = s.discretize(normalized);
		System.out.println("Finished normalizing, Discretizing....\n");
		
		/*try{
			PrintWriter writer = new PrintWriter("666.txt", "UTF-8");
			for(String z : dtrain)
				writer.println(z);
			writer.close();
		} catch (Exception e) {
		   // do something
		}*/

DataHolder dh = new DataHolder(dt, null);
        System.out.println("finished reading and cleaning data\nBuilding tree...");

        Date dtStartBuildTree = new Date();
        SimpleNode node = s.buildtree(null, dh, null, null);
        Date dtEndBuildTree = new Date();

        System.out.println("built tree\nreading test data...");
        //node.printNode(node);
        // validation begins
        ArrayList<String> autompg_test = s.readCSVFile("..\\data\\eval\\2008_test1.txt");
        //ArrayList<String> autompg_test = s.readCSVFile("zoo12.test");
        //ArrayList<String> test = s.normalize(autompg_test);
        //object classifiedNode = null;
        //ArrayList<String> dtest = s.discretize(test);
        System.out.println("finished reading and cleaning test\nstarting classification...");
        HashMap<Integer, String> testingNodesList = new HashMap<Integer, String>();
        HashMap<Integer, String> classifiedNodesList = new HashMap<Integer, String>();

        Date dtStartClassify = new Date();
        int i = 0;
        for (String datarow:autompg_test)
        {
            testingNodesList.put(i, (String)datarow.split(splitChar)[datarow.split(splitChar).length - 1]);
            Object classifiedNode = s.classify(datarow, node);
            classifiedNodesList.put(i, classifiedNode instanceof SimpleNode ? (((SimpleNode)classifiedNode).Name) : (String)classifiedNode);
            String c= classifiedNodesList.get(i);
            System.out.println(String.join(",", datarow) + "\t" + c.charAt(c.length()-1));
            i++;
        }
        Date dtEndClassify = new Date();
        System.out.print("\nfinished classifying\ncalculating accuracy...");
        //System.out.print("\nfinished classifying");
        int predictedCorrectValues = 0;
        for (int m = 0; m < testingNodesList.size(); m++)
            if (testingNodesList.get(m).equals(classifiedNodesList.get(m)))
                predictedCorrectValues += 1;

        double accuracy = 0;
        if (testingNodesList.size() != 0)
            accuracy = (float)(predictedCorrectValues) / testingNodesList.size() * 100;
        System.out.print("\nFound Accuracy:" + accuracy + " %");

        long buildTime = dtEndBuildTree.getTime() - dtStartBuildTree.getTime();
        long classifyTime = dtEndClassify.getTime() - dtStartClassify.getTime();
        System.out.println("\nTime taken to buildtree:"+buildTime+"ms \nTime taken to classify:"+classifyTime+"ms");
        
        //Console.ReadKey();
    }
}
