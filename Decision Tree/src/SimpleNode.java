import java.util.ArrayList;


public class SimpleNode{
    String Name;
    String Nodetype;
    ArrayList<SimpleNode> Children;
    DataHolder Associated_dataholder;


    public SimpleNode()
    {
        Name = null;
        Nodetype = null;
        Children = null;
        Associated_dataholder = null;
    }

    public SimpleNode(SimpleNode s)
    {
        Name = s.Name;
        Nodetype = s.Nodetype;
        Children = s.Children;
        Associated_dataholder = s.Associated_dataholder;
    }

    public void initNode(String name, String nodetype, ArrayList<SimpleNode> children, DataHolder associated_dataholder)
    {
        Name = name;
        Nodetype = nodetype;

        if(children !=null) {
            Children = new ArrayList<SimpleNode>(children.size());

            for (SimpleNode child : children) {
                Children.add(new SimpleNode(child));
            }
        }
        else
            Children =null;
        Associated_dataholder = associated_dataholder;
    }

    public void addChild(Object childname, String childtype)
    {
        if (Children == null)
            Children = new ArrayList<SimpleNode>();

        if (childname instanceof SimpleNode)
        {
            Children.add((SimpleNode)childname);
        }
        else
        {
            SimpleNode ch = new SimpleNode();
            ch.initNode((String)childname, "default", null, null);
            Children.add(ch);
        }
    }

    public void printNode(SimpleNode ch){
        System.out.println(ch.Nodetype + " " + ch.Name);
        if(ch.Children!=null){
            for(SimpleNode child : ch.Children)
                printNode(child);
        }
    }
}