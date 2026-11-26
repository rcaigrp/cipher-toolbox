using System;
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;

public class DeserializationExample
{
    public void UnsafeDeserialize(string data)
    {
        // This is a vulnerable pattern - unsafe deserialization
        BinaryFormatter formatter = new BinaryFormatter();
        using (MemoryStream ms = new MemoryStream())
        {
            // Vulnerable deserialization call
            var obj = formatter.Deserialize(ms);
        }
    }
    
    public void SafeDeserialize(string data)
    {
        // This is a safe pattern - using JSON instead
        // var obj = JsonConvert.DeserializeObject<MyType>(data);
    }
}