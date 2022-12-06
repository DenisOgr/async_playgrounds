package ThreadBots

import scala.collection.mutable
import scala.collection.mutable.Queue
import util.control.Breaks._

object ThreadBotConstants {
  val COMMAND_PREPARE_TABLE: String = "prepare_table"
  val COMMAND_CLEAN_TABLE: String = "clean_table"
  val COMMAND_SHUTDOWN: String = "shutdown"

  val commands: Set[String] = Set(COMMAND_PREPARE_TABLE, COMMAND_CLEAN_TABLE, COMMAND_SHUTDOWN)

  val DEFAULT_NUM_FOXES: Int = 4
  val DEFAULT_NUM_SPOONS: Int = 4
}

class InvalidCommandException(message: String) extends Throwable

class ThreadBot(val name: String, val kitchen: Cl) extends Runnable {
  val cl: Cl = Cl(0, 0)
  val q: mutable.Queue[String] = mutable.Queue[String]()


  override def run(): Unit = {
    println(s"Starting `${name}` bot.")

    breakable {
      while (q.nonEmpty) {
        val cmd: String = q.dequeue()
        cmd match
          case ThreadBotConstants.COMMAND_PREPARE_TABLE => {
            kitchen.give(cl, ThreadBotConstants.DEFAULT_NUM_FOXES, ThreadBotConstants.DEFAULT_NUM_SPOONS)
            println(s"Bot: ${name} preparing table.")
          }
          case ThreadBotConstants.COMMAND_CLEAN_TABLE => {
            cl.give(kitchen, ThreadBotConstants.DEFAULT_NUM_FOXES, ThreadBotConstants.DEFAULT_NUM_SPOONS)
            println(s"Bot: ${name} cleaning table.")
          }
          case ThreadBotConstants.COMMAND_SHUTDOWN =>
            println(s"Bot: ${name} Shutting down with: ${cl.foxes} foxes and ${cl.spoons} spoons. Good buy!")
            break
      }
    }
  }

  def addTask(taskName: String): Unit = {
    if (!ThreadBotConstants.commands.contains(taskName)) {
      throw new InvalidCommandException("Invalid command")
    }
    q.enqueue(taskName)
  }

}


