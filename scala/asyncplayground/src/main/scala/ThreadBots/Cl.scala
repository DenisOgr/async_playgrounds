package ThreadBots

class Cl (var foxes: Int, var spoons: Int) {

  def give(cl: Cl, num_foxes: Int, num_spoons: Int): Unit = {
    change(-num_foxes, -num_spoons)
    cl.change(num_foxes, num_spoons)
  }

  def change(num_foxes: Int, num_spoons: Int): Unit = {
    foxes += num_foxes
    spoons += num_spoons
  }

  override def toString: String = {
    s"Cl object with ${foxes} foxes and ${spoons} spoons."
  }
}
