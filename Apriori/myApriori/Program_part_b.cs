using System;
using System.Collections.Generic;
using System.Data;
using System.IO;
using System.Linq;

using System.Diagnostics;
using System.Runtime.InteropServices;

using Facet.Combinatorics;

using kValue = System.Int32;
using ItemSet = System.String;
using Support = System.Single;
using System.Text;

namespace myApriori
{
    public class DataHandler
    {
        #region Custom Types
        enum Metric { SupportCount, Support, Confidence }
        enum Delimiter { Comma, Tab }
        enum AprioriMethod { Km1K1, Km1Km1 }
        #endregion

        #region private properties
        private float _minsup;
        //private int _k;
        private DataTable _inputDataset;
        private DataTable _sparseMatrix;
        private List<ItemSet> _columnNames = new List<ItemSet>();

        private Dictionary<kValue, Dictionary<ItemSet, Support>> _candidateItemSets = new Dictionary<kValue, Dictionary<ItemSet, Support>>();
        private Dictionary<kValue, Dictionary<ItemSet, Support>> _candidateItemSubSets = new Dictionary<kValue, Dictionary<ItemSet, Support>>();
        private Dictionary<kValue, Dictionary<ItemSet, Support>> _frequentItemSets = new Dictionary<kValue, Dictionary<ItemSet, Support>>();
        #endregion

        #region private methods
        private void SetInitialCandidateAndFrequentSets()
        {
            Dictionary<ItemSet, Support> oneItemCandidateSet = new Dictionary<ItemSet, Support>();
            Dictionary<ItemSet, Support> oneItemFrequentSet = new Dictionary<ItemSet, Support>();

            foreach (ItemSet itemSet in _columnNames)
            {
                float sup = getMetricValue(itemSet, Metric.Support);
                oneItemCandidateSet.Add(itemSet, sup);
                if (sup >= _minsup)
                {
                    oneItemFrequentSet.Add(itemSet, sup);                    
                }                
            }
            _candidateItemSets[0] = oneItemCandidateSet; // update this also to handle the array index vs key properly like frequent itemset
            _frequentItemSets[0] = oneItemFrequentSet;
        }

        //private void Generate_k_CandidateItemsets(kValue k)
        private void GenerateNextCandidateItemsets(int k, AprioriMethod apm) //operates on kth frequent itemset _frequentItemSets[k]
        {
            switch (apm)
            {

                case AprioriMethod.Km1K1:
                    foreach (KeyValuePair<ItemSet, Support> kvp in _frequentItemSets[k - 1])
                    {
                        Dictionary<ItemSet, Support> dict = new Dictionary<ItemSet, Support>();
                        foreach (ItemSet column in _columnNames)
                        {
                            ItemSet[] splitArr = kvp.Key.Split(',');
                            if (!splitArr.Contains(column)) //if column not in kvp.key
                            {
                                ItemSet combinedColumn = kvp.Key + ',' + column;
                                Support metricSupport = getMetricValue(combinedColumn, Metric.Support);
                                /*if (metricSupport >= _minsup)//if combined column's support is more than minsup
                                {
                                    candidates.Add(combinedColumn);//add it to kvp.key
                                    NextCandidateItemSet.Add(combinedColumn, metricSupport);
                                }*/
                                dict.Add(combinedColumn, metricSupport);
                            }
                        }
                        _candidateItemSets[k] = dict;
                    }
                    break;

                case AprioriMethod.Km1Km1:
                    foreach (KeyValuePair<ItemSet, Support> kvp in _frequentItemSets[k - 1])
                    {
                        Dictionary<ItemSet, Support> dict = new Dictionary<ItemSet, Support>();
                        foreach (ItemSet column in _columnNames)
                        {
                            ItemSet[] splitArr = kvp.Key.Split(',');
                            if (!splitArr.Contains(column)) //if column not in kvp.key
                            {
                                ItemSet combinedColumn = kvp.Key + ',' + column;
                                Support metricSupport = getMetricValue(combinedColumn, Metric.Support);
                                /*if (metricSupport >= _minsup)//if combined column's support is more than minsup
                                {
                                    candidates.Add(combinedColumn);//add it to kvp.key
                                    NextCandidateItemSet.Add(combinedColumn, metricSupport);
                                }*/
                                dict.Add(combinedColumn, metricSupport);
                            }
                        }
                        _candidateItemSets[k] = dict;
                    }
                    break;
            }
        }

        private void Generate_k_FrequentItemSets(kValue k)
        {
            Console.WriteLine("Generating Frequent Itemsets:");
            //k--;    //_freqItemSets[0] has frequent 1 itemset so update k once to get to the right position
            if (k > 1) //start calculating for frequent 2 itemsets and further because frequent 1 itemset has already been generated at initialization
            {
                //foreach (KeyValuePair<ItemSet, Support> kvp in _frequentItemSets[k - 1])
                foreach (KeyValuePair<ItemSet, Support> kvp in GetFrequentItemSets(k - 1))
                {
                    //GenerateCandidateItemsets(k);
                    Dictionary<ItemSet, Support> freqItemSets = new Dictionary<ItemSet, Support>();
                    foreach (ItemSet itemSet in _columnNames)
                    {
                        float sup = getMetricValue(itemSet, Metric.SupportCount);
                        if ((int)sup >= _minsup)
                        {
                            freqItemSets.Add(kvp.Key + "," + itemSet, sup);
                        }
                    }
                    _frequentItemSets.Add(k-1, freqItemSets);
                }
            }
            Console.WriteLine("Finished generating Frequent Itemsets:");
        }

        private Dictionary<ItemSet, Support> GetFrequentItemSets(int k)
        {
            return _frequentItemSets[k - 1]; // _frequentItemSets[0] contains 1item frequesnt set, _frequentItemSets[1] contains 2 item frequent set and so on...
        }

        private void SetFrequentItemSets(int k, Dictionary<ItemSet, Support> d)
        {
            _frequentItemSets[k - 1] = d; // _frequentItemSets[0] contains 1item frequesnt set, _frequentItemSets[1] contains 2 item frequent set and so on...
        }

        private Support getMetricValue(ItemSet val, Metric m)
        {
            ItemSet[] splitItems = val.Split(',');
            if (splitItems.Length == 1)
            {
                switch (m)
                {
                    case Metric.SupportCount:
                        float x = Convert.ToInt32(this._sparseMatrix.Compute("COUNT([" + val + "])", val + "= 1"));
                        return x;

                    case Metric.Support:
                        float y = Convert.ToInt32(this._sparseMatrix.Compute("COUNT([" + val + "])", "[" + val + "] = 1"));
                        return (y / this._sparseMatrix.Rows.Count);

                    case Metric.Confidence: return 0;
                    default: return 0;
                }
            }
            else
            {
                switch (m)
                {
                    case Metric.Support:
                        StringBuilder query = new StringBuilder("[");
                        foreach (ItemSet item in splitItems)
                        {
                            query.Append(item);
                            query.Append("] = 1 AND [");
                        }
                        query.Remove(query.Length - 5, 5);
                        DataRow[] drColln = _sparseMatrix.Select(query.ToString());
                        if (drColln.Length > 0)
                        {
                            return (float)drColln.Length / _sparseMatrix.Rows.Count;
                        }
                        else
                            return 0;

                    default: return 0;
                }
            }
        }

        private void pruneFrequentCandidatesBySupport(int length)
        {
            throw new NotImplementedException();
        }

        private void calculateSupportCounts(int length)
        {
            throw new NotImplementedException();
        }

        //private Dictionary<ItemSet, Support> GetFrquntCandidatesPrunedBySubsetSupport(int length, int k)
        //{
        //    foreach(KeyValuePair<ItemSet, Support> kvp in _candidateItemSubSets[length])
        //    {
        //        if (kvp.Value >= _minsup)
        //        {
        //            _frequentItemSets.Add(length, kvp.Value);
        //        }
        //    }
        //}

        //private void GenerateCandidateSubSetsWithSupports(kValue k)
        //{
        //    foreach (KeyValuePair<ItemSet, Support> kvp in _frequentItemSets[k])
        //    {
        //        List<ItemSet> l = kvp.Key.Split(',').ToList();
        //        Combinations<ItemSet> combinations = new Combinations<ItemSet>(l, k - 1, GenerateOption.WithoutRepetition);
                
        //        foreach (IList<ItemSet> c in combinations)
        //        {
        //            ItemSet res = string.Join(",", c);
        //        }
        //        _candidateItemSubSets.Add(k, res);
        //    }
        //}

        #endregion

        #region public methods

        public DataHandler()
        {
            _inputDataset = new DataTable();
            _sparseMatrix = new DataTable();
            _minsup = 0.5f;
            //SetInitialCandidateAndFrequentSets();
        }

        public DataHandler(float inputMinSup)
        {
            _inputDataset = new DataTable();
            _sparseMatrix = new DataTable();
            _minsup = inputMinSup;
            //SetInitialCandidateAndFrequentSets();
        }

        public void ReadInput(string FilePath, char delimiter)
        {
            Console.WriteLine("Reading input...");
            int columnsCount = 0;
            using (StreamReader srcheck = new StreamReader(FilePath))
            {
                string firstLine = Convert.ToString(srcheck.ReadLine());
                string[] splitArr = firstLine.Split(delimiter);
                columnsCount = splitArr.Length;
                splitArr = null;
                srcheck.Close();
            }
            using (StreamReader sr = new StreamReader(FilePath))
            {
                string firstLine = Convert.ToString(sr.ReadLine());
                for (int c = 0; c < columnsCount; c++)
                {
                    this._inputDataset.Columns.Add("col" + c);
                }

                var DSFileContents = File.ReadAllLines(FilePath).ToList();
                DSFileContents.ForEach(DSRow => _inputDataset.Rows.Add(DSRow.Split(delimiter)));

                sr.Close();
            }
            Console.WriteLine("...finished reading input");
        }

        public void DisplayInputDataset()
        {
            Console.WriteLine("\nStarted input dataset display");
            foreach (DataRow row in this._inputDataset.Rows)
            {
                foreach (var item in row.ItemArray)
                {
                    Console.Write(item + ",");
                }
                Console.WriteLine();
            }
            Console.WriteLine("Number of rows:" + this._inputDataset.Rows.Count + "\nEnded input dataset display");
        }

        public void CreateSparseMatrix()
        {
            Console.WriteLine("\nGenerating Sparse Matrix...");


            #region CreateBlankSparseMatrix
            foreach (DataRow row in this._inputDataset.Rows)
            {
                //find unique number of values in the dataset --> rowmax - probably need to store the dataset in a separate dictionary
                //create rowmax number of columns in the sparsematrix
                _sparseMatrix = new DataTable();
                for (int j = 0; j < this._inputDataset.Columns.Count; j++)
                {
                    string temp = Convert.ToString(row[j]).Trim();
                    //for each value in the values dictionary
                    //check if it is present in the current row under consideration    
                    if (!String.IsNullOrEmpty(temp))
                    {
                        if (!_columnNames.Contains(temp))
                        {
                            _columnNames.Add(temp);
                        }
                    }
                }
            }
            #endregion

            //if so, set bool to true for the row for the given value's corresponding column
            foreach (string valu in _columnNames)
            {
                _sparseMatrix.Columns.Add(valu, Type.GetType("System.Int32"));
            }

            //create same number of rows and initialize
            for (int i = 0; i < this._inputDataset.Rows.Count; i++)
            {
                DataRow dr = _sparseMatrix.NewRow();
                _sparseMatrix.Rows.Add(dr);
            }

            //columns added, now add rows with 0/1 values
            int counter = 0;
            foreach (DataRow row in _sparseMatrix.Rows)
            {
                foreach (DataColumn col in _sparseMatrix.Columns)
                {
                    _sparseMatrix.Rows[counter][col.ColumnName] = (_inputDataset.Rows[counter].ItemArray.Contains(col.ColumnName)) ? 1 : 0;
                }
                counter++;
            }
            Console.WriteLine("Sparse Matrix generation complete");
        }

        public void DisplaySparseMatrix()
        {
            Console.WriteLine("\nStarted Sparse Matrix display:");
            using (StreamWriter sw = new StreamWriter("_columnNames.txt"))
            {
                foreach (ItemSet itm in _columnNames)
                {
                    sw.WriteLine(itm);
                }
                sw.Close();
            }
            using (StreamWriter sw = new StreamWriter("sparsemat.xls"))
            {
                foreach (DataColumn dc in _sparseMatrix.Columns)
                {
                    Console.Write(dc.ColumnName + "\t");
                    sw.Write(dc.ColumnName + "\t");
                }
                sw.WriteLine();
                foreach (DataRow row in _sparseMatrix.Rows)
                {
                    for (int j = 0; j < _sparseMatrix.Columns.Count; j++)
                    {
                        //Console.WriteLine(j);
                        Console.Write(row[j] + " ");
                        sw.Write(row[j] + "\t");
                    }
                    Console.WriteLine();
                    sw.WriteLine();
                }
                Console.WriteLine("Number of rows:" + _sparseMatrix.Rows.Count + "\nEnded Sparse Matrix display");
                sw.WriteLine("Number of rows:" + _sparseMatrix.Rows.Count + "\nEnded Sparse Matrix display");
                sw.Close();
            }
        }

        public void Apriori(kValue kval)
        {
            Console.WriteLine("\nGenerating Frequent itemsets...");
            //_k = kval + 1;
            SetInitialCandidateAndFrequentSets();//initializes _candidateItemSets[0] manually and _frequentItemSets[0] based on condidates itemset support count
            for (int k = 1; k < kval; k++)
            {
                //_candidateItemSets[1] = GenerateKPlusOneCandidateItemsets(0);

                GenerateNextCandidateItemsets(k, AprioriMethod.Km1K1);//has to operate on kth frequent itemset _frequentItemSets[k]

                //_frequentItemSets[1] = GetFrquntCandidatesPrunedBySubsetSupport(1, kval);
                //Generate subsets of candidateItemSet and prune candidate itemsets containing subsets of length k that are infrequent       //GetFrquntCandidatesPrunedBySubsetSupport(k + 1, kval);    // has to operate on k+1th candidate itemset _candiateItemSets[k+1]
                Dictionary<ItemSet, Support> d = new Dictionary<string, float>();
                foreach (KeyValuePair<ItemSet, Support> kvp in _candidateItemSets[k - 1])
                {
                    bool retain = true;
                    Combinations<string> subsets = new Combinations<string>(kvp.Key.Split(','), k, GenerateOption.WithoutRepetition);
                    ItemSet[] arr = kvp.Key.Split(',');

                    if (subsets.Count > 0)
                    {
                        foreach (IList<ItemSet> subset in subsets)
                        {
                            float supportOfSubset = getMetricValue(string.Join(",", subset[0]), Metric.Support);
                            if (supportOfSubset < _minsup)
                            {
                                retain = false;
                                break;
                            }
                        }

                        if (retain)
                        {
                            d.Add(kvp.Key, kvp.Value);
                        }
                    }
                }
                _frequentItemSets.Add(k, d);

                
                List<ItemSet> toBeDeleted = new List<ItemSet>();
                foreach (KeyValuePair<ItemSet, Support> kvp in _frequentItemSets[k])
                {
                    float supportOfSuperSet = getMetricValue(kvp.Key, Metric.Support);
                    if (supportOfSuperSet < _minsup)
                    {
                        toBeDeleted.Add(kvp.Key);
                    }
                }

                //eliminate the candidates that are infrequent to leave only the frequent itemsets
                ///pruneFrequentCandidatesBySupport(k + 1);//has to operate on k+1th frequent itemset _frequentItemSets[k+1]
                //foreach(ItemSet itm in toBeDeleted)
                //{
                //    if (_frequentItemSets.ContainsKey(k))
                //    {
                //        _frequentItemSets[k].Remove(itm);
                //    }
                //}
            }
            for (int x = 0; x < _frequentItemSets.Count; x++)
            {
                foreach (KeyValuePair<string, float> kvpp in _frequentItemSets[x])
                {
                    if (getMetricValue(kvpp.Key, Metric.Support) < _minsup)
                    {
                        _frequentItemSets[x].Remove(kvpp.Key);
                        break;
                    }
                }
            }
            Console.WriteLine("\n...Finished generating frequent itemsets");
        }

        public void DisplayFrequentkItemSets()
        {
            //Generate_k_FrequentItemSets(k);
            Console.WriteLine("\nDisplaying Frequent Itemsets:\nItemSet \t\t Support Count\n");
            List<ItemSet> Displayed = new List<ItemSet>();
            for (int u = 0; u < _frequentItemSets.Count; u++)
            {
                foreach (KeyValuePair<ItemSet, Support> kvp in _frequentItemSets[u])
                {
                    if (kvp.Value >= _minsup)
                        if (!Displayed.Contains(kvp.Key))
                        {
                            Console.WriteLine(kvp.Key + " \t\t " + kvp.Value);
                            Displayed.Add(kvp.Key);
                        }
                }
            }
            Console.WriteLine("\nFinished displaying Frequent Itemsets");
        }

        #endregion

        #region __
        //Generate itemsets of given size
        //public Dictionary<ItemSet, Support> GenerateItemSet(int k)
        //{
        //    Dictionary<ItemSet, Support> ItemSets = new Dictionary<ItemSet, Support>();
        //    ItemSets = GetFrequentItemSets(k);
        //    if (k == 1)
        //    {
        //        return ItemSets;
        //    }
        //    else
        //    {
        //        List<ItemSet> retSet = new List<ItemSet>();
        //        for (int i = 0; i < k; i++)
        //        {

        //        }
        //        return null;
        //    }
        //}

        #region futurework
        //extra work
        //To convert sparsematrix into CSR or CSC format
        //public CompressSparseMatrix()
        //{

        //}
        #endregion

        #endregion
    }

    public class Program
    {
        [DllImport("user32.dll")]
        public static extern bool ShowWindow(System.IntPtr hWnd, int cmdShow);

        private static bool isUserOK(string msg)
        {
            Console.Write("\nDisplay "+ msg + " ?Y/N(or any other key to continue):");
            ConsoleKeyInfo ckiInputDS = Console.ReadKey();
            if (ckiInputDS.KeyChar == 'y' || ckiInputDS.KeyChar == 'Y')
                return true;
            return false;
        }

        private void WorkOnFile(string FilePath, char delimiter, float minsup, int kVal)
        {
            DataHandler dh = new DataHandler(minsup);//input minsup - default is 0.5      //dh.ReadInput("Concrete.txt");//read to internal inputDataItemset
            dh.ReadInput(FilePath, ',');

            if (isUserOK("input dataset"))
                dh.DisplayInputDataset();

            dh.CreateSparseMatrix();

            if (isUserOK("Sparse Matrix"))
                dh.DisplaySparseMatrix();

            dh.Apriori(kVal); //Apriori for two itemsets
            if (isUserOK("Frequent Item Sets"))
                dh.DisplayFrequentkItemSets();

            dh = null;
        }

        public static void Main(string[] args)
        {
            Process p = Process.GetCurrentProcess();
            ShowWindow(p.MainWindowHandle, 3); //SW_MAXIMIZE = 3
            Console.WriteLine("Begin program");
            float minsup = 0.5f;
            Console.Write("Enter minsup value:");
            try { minsup = (float)Convert.ToDouble(Console.ReadLine()); }
            catch (FormatException) { minsup = 0.5f; }
            catch (InvalidCastException) { minsup = 0.5f; }
            catch (InvalidOperationException) { minsup = 0.5f; }

            Program pgrm = new Program();
            pgrm.WorkOnFile("car.data", ',', 0.05f, 7);// > 1000
            pgrm.WorkOnFile("nursery.data", ',', 0.05f, 7);// > 10000
            pgrm.WorkOnFile("kr-vs-kp.data", ',', 0.05f, 7);

            //pgrm.WorkOnFile("seismic-bumps.arff", ' ', 0.05f, 7);

            Console.WriteLine("End program");
            Console.ReadKey();//wait for user before exit
        }
    }
}