using System;
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;

public class TestDeserialization
{
    public static void Main()
    {
        // This is a test file that uses BinaryFormatter - should be detected
        BinaryFormatter formatter = new BinaryFormatter();
        Console.WriteLine("Test file with BinaryFormatter");
    }
}