package ThreadBots
import ThreadBots.Cl, ThreadBots.ThreadBot

object Main {
  val defaultNumberOfTables: Int = 100_000
  val defaultNumberOfBots: Int = 10

  def main(args: Array[String]): Unit = {
    val numberOfTables: Int = if (args.length > 0) args(0).toInt else defaultNumberOfTables
    val numberOfBots: Int = if (args.length > 1) args(1).toInt else defaultNumberOfBots
    val kitchen: Cl = Cl(100, 100)

    println(s"There are ${kitchen.foxes} foxes and ${kitchen.spoons} spoons in the kitchen in the BEGINNING of the day.")

    val bots: List[ThreadBot] = (1 to numberOfBots).map(i =>  ThreadBot(s"Bot#${i}", kitchen)).toList
    for (bot <- bots) {
      for (_ <- 1 to numberOfTables) {
        bot.addTask(ThreadBotConstants.COMMAND_PREPARE_TABLE)
        bot.addTask(ThreadBotConstants.COMMAND_CLEAN_TABLE)
      }
      bot.addTask(ThreadBotConstants.COMMAND_SHUTDOWN)
    }
    val bot_threads = bots.map(bot => Thread(bot))
    bot_threads.foreach(thread => thread.start())
    bot_threads.foreach(thread => thread.join())

    println(s"There are ${kitchen.foxes} foxes and ${kitchen.spoons} spoons in the kitchen in the ENG of the day.")
  }
}
