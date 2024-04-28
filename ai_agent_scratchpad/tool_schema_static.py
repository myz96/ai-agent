# Define tool schema
tools_static = [
    {
        "type": "function",
        "function": {
            "name": "extract_profile_information",
            "description": "Extracts profile information from a private CRM. Use this tool when you need to extract profile information from a prospect lead.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": f"""
                                Name of the prospect lead.
                                """,
                    }
                },
                "required": ["name"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_email_thread_id",
            "description": "Finds the approprate email_thread_id for a prospect lead. This MUST be called if we want to retrieve a prospect's previous emails. Use this tool when you need to find the email thread ID for a prospect lead.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": f"""
                                Name of the prospect lead.
                                """,
                    }
                },
                "required": ["name"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "retrieve_relevant_value_prop",
            "description": "Retrieves relevant value propositions from a private vector database. Use this tool when you need to retrieve relevant value propositions for a prospect lead.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": f"""
                                Name of the prospect lead.
                                """,
                    }
                },
                "required": ["name"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "retrieve_email_thread_content",
            "description": "Retrieves email thread content from a private email database. Use this tool when you need to retrieve previous email thread content using the email thread ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": f"""
                                Name of the prospect lead.
                                """,
                    }
                },
                "required": ["name"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compose_outreach_email",
            "description": "Composes an outreach email to the propsect lead leveraging existing information that combines all relevant information about the prospect including their profile information, their unique value propositon and their previous email content. Use this tool when you need to compose an outreach email to a prospect lead.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": f"""
                                Name of the prospect lead.
                                """,
                    }       
                },
                "required": ["name"],
            },
        }
    },
]
