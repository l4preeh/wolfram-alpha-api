
def parse_response(data):
    query_result = data.get("queryresult", {})
    pods = query_result.get("pods", [])

    results = []

    for pod in pods:
        title = pod.get("title", "")
        subpods = pod.get("subpods", [])

        pod_texts = []

        for subpod in subpods:
            text = subpod.get("plaintext", "")

            if text:
                pod_texts.append(text)

        results.append({
            "title": title,
            "text": pod_texts
        })

    return {
        "success": True,
        "results": results
    }
