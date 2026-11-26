using System.Text.Json;

public static class SafeDeserializationExample
{
    public sealed class SampleData
    {
        public string Name { get; set; } = string.Empty;
    }

    public static SampleData Parse(string json)
    {
        return JsonSerializer.Deserialize<SampleData>(json) ?? new SampleData();
    }
}
