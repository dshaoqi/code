package dsq.test;
import akka.actor.ActorRef;
import akka.actor.ActorSystem;
import akka.actor.AbstractActor;
import akka.event.Logging;
import akka.event.LoggingAdapter;
import akka.actor.Props;
import java.io.IOException;
//public class hellowWorld{
  public class Printer extends AbstractActor{
    static public Props props(){
       return Props.create(Printer.class,()->new Printer());
    }
    //message
    static public class Greeting{
       public final String Message;
       public Greeting(String Message){
         this.Message=Message;
       } 
    }

    private LoggingAdapter log=Logging.getLogger(getContext().getSystem(),this);  
 
    public Printer(){
    } 
   
    public Receive createReceive(){
       return receiveBuilder()
	.match(Greeting.class,greeting->{log.info(greeting.Message);})
        .build();
    } 
  }
  
 /* public class Greeter extends AbstractActor{
    static public Props props(ActorRef printerActor){
      return Props.create(Greeter.class,()->new Greeter(printerActor));
    }
    
    static public class Message1{
      public final String who;
      public Message1(String who){
        this.who=who;
      }
    }

    static public class Message2{
      public  int a=0;
      public Message2(){
        a++;
      }
    }
    
    public ActorRef printerActor;
    private String who;
    private int k; 

    public Greeter(ActorRef pri){
      printerActor=pri;
    }   

    public Receive createReceive(){
      return receiveBuilder()
	.match(Message1.class,x->{this.who=x.who;})
	.match(Message2.class,y->{this.k=y.a;System.out.println("k="+this.k);})
	.build();
    } 
  }
  
  public static void main(String[] args){
    final ActorSystem sys=ActorSystem.create("test");
    try{
      final ActorRef printer=sys.actorOf(Printer.props(),"priActor");
      final ActorRef greeter=sys.actorOf(Greeter.props(printer),"greeterActor");
      printer.tell(new Greeting("heihei"),ActorRef.noSender());
    }catch(IOException ioe){
      
    }finally{
      sys.terminate();
    }
  }

}*/
