function process_record(tag, timestamp, record)
    local container_name = record["container_name"]
    if container_name then
        local extracted_name = container_name:match("/12%-factor%-app%-(.+)$")
        if extracted_name then
            record["container"] = extracted_name
        end
    end
    return 1, timestamp, record
end
